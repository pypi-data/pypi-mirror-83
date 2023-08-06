# coding=utf-8
# Copyright 2020 The jax_verify Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
# pylint: disable=invalid-name
"""Small helper functions."""

import collections
import copy
import enum
import functools

import jax
import jax.lax as lax
import jax.numpy as jnp
import numpy as np
import optax
import tree

IntBound = collections.namedtuple(
    'IntervalBound', ['lb', 'ub', 'lb_pre', 'ub_pre'])
_AdvRobustnessVerifInstance = collections.namedtuple(
    'VerifInstance',
    ['params', 'params_full', 'input_bounds', 'bounds', 'obj', 'obj_orig',
     'const', 'type'])
_VerifInstance = _AdvRobustnessVerifInstance  # alias
_SdpDualVerifInstance = collections.namedtuple(
    'SdpDualVerifInstance',
    ['bounds', 'make_inner_lagrangian', 'dual_shapes', 'dual_types'])


class SdpDualVerifInstance(_SdpDualVerifInstance):
  """A namedtuple specifying a verification instance for the dual SDP solver.

  Fields:
    * bounds: A list of bounds on post-activations at each layer
    * make_inner_lagrangian: A function which takes ``dual_vars`` as input, and
      returns another function, the inner lagrangian, which evaluates
      Lagrangian(x, dual_vars) for any value ``x`` (the set of activations).
    * dual_types: A pytree matching dual_vars specifying which dual_vars
      should be non-negative.
    * dual_shapes: A pytree matching dual_vars specifying shape of each var.
  """


default_conv_transpose = functools.partial(
    lax.conv_transpose, dimension_numbers=('NHWC', 'HWIO', 'NHWC'))

################## Networks ######################


def mlp_layer_sizes(params):
  # Dimension of input to each layer, and output of final layer
  layer_sizes = [int(w.shape[0]) for (w, b) in params]
  fin_w, _ = params[-1]
  layer_sizes.append(int(fin_w.shape[1]))
  return layer_sizes


def nn_layer_sizes(params):
  """Compute MLP sizes of the inputs/outputs for individual layers."""
  assert not any([isinstance(x, dict) for x in params]), 'MLP only'
  return mlp_layer_sizes(params)


def layer_sizes_from_bounds(bounds):
  assert all([b.lb.shape[0] == 1 for b in bounds])
  layer_sizes = [b.lb.shape[1:] for b in bounds]
  layer_sizes = [s[0] if len(s) == 1 else s for s in layer_sizes]
  return layer_sizes


def predict_mlp(params, inputs):
  for W, b in params[:-1]:
    outputs = jnp.dot(inputs, W) + b
    inputs = jnp.maximum(outputs, 0)
  W, b = params[-1]
  return jnp.dot(inputs, W) + b


def fwd(inputs, layer_params):
  """JAX forward pass of Linear, Conv, or ConvTranspose."""
  if isinstance(layer_params, dict):
    # Conv/ConvTranspose: Reshape input if necessary:
    if len(inputs.shape) < 4:
      w = h = int(np.sqrt(inputs.shape[-1]/layer_params['n_cin']))
      inputs = inputs.reshape(inputs.shape[0], h, w, layer_params['n_cin'])
    W, b = layer_params['W'], np.reshape(layer_params['b'], [1, 1, 1, -1])
    if 'transpose' in layer_params and layer_params['transpose']:
      # ConvTranspose
      return default_conv_transpose(
          inputs, W, (layer_params['stride'], layer_params['stride']),
          layer_params['padding']) + b
    else:
      # Normal Conv2D
      dn = lax.conv_dimension_numbers(inputs.shape, W.shape,
                                      ('NHWC', 'HWIO', 'NHWC'))
      return lax.conv_general_dilated(
          inputs, W, (layer_params['stride'], layer_params['stride']),
          layer_params['padding'], (1, 1), (1, 1), dn) + b
  elif isinstance(layer_params, tuple):
    # Linear fully-connected layer
    # TODO: Figure out why we were dropping batch dim before here
    inputs = (inputs.reshape(inputs.shape[0], -1)
              if len(inputs.shape) == 4 else inputs)
    (W, b) = layer_params
    return jnp.dot(inputs, W) + b
  else:
    raise NotImplementedError('Unknown layer')


def predict_cnn(params, inputs, include_preactivations=False):
  """Forward pass for a CNN given parameters.

  Args:
    params: Parameters for the CNN. See make_cnn_params for syntax.
    inputs: Inputs to CNN.
    include_preactivations: bool. If True, also return pre-activations after
      each matmul layer.
  Returns:
    act: Output from forward pass through CNN.
    (Optional) layer_acts: Post-relu activation at each layer
  """
  act = inputs
  layer_preacts = []
  for counter, layer_params in enumerate(params):
    act = fwd(act, layer_params)
    layer_preacts.append(act)
    if counter < len(params) - 1:
      # no relu on final layer
      act = jnp.maximum(act, 0)
  return act if not include_preactivations else (act, layer_preacts)


def get_network_activs(params, x):
  assert len(x.shape) == 1, 'x should not have batch dim'
  activs = [x]
  for W, b in params:
    x = jnp.matmul(x, W) + b
    x = jnp.maximum(x, 0.)
    activs.append(x)
  return activs


def get_layer_params(fun_to_extract, example_input):
  """Extract the parameters from a network specified as a function.

  Args:
    fun_to_extract: Function implementing a simple MLP/CNN network composed
      of alternating linear layers and ReLU activation functions.
    example_input: Example of input to `fun_to_extract`.
  Returns:
    params: Parameters for the CNN/MLP, as taken by `predict_cnn` or
      `predict_mlp`
  """
  jaxpr_maker = jax.make_jaxpr(fun_to_extract)
  parsed = jaxpr_maker(example_input)

  layers = []
  next_is_relu = False
  scaling = None
  centering = None

  jax_parameters = {var: param_vals
                    for var, param_vals in zip(parsed.jaxpr.constvars,
                                               parsed.literals)}
  def _get_const_input_arg(eqn):
    if eqn.invars[0] in jax_parameters:
      return eqn.invars[0]
    elif eqn.invars[1] in jax_parameters:
      return eqn.invars[1]
    else:
      raise ValueError('None of the primitive\'s input is a weight tensor.')

  for eqn in parsed.jaxpr.eqns:
    if eqn.primitive == lax.reshape_p:
      if eqn.invars[0] in jax_parameters:
        # If this is a reshaping of a constant / the input of the reshape will
        # be in the jax_parameters dict. We can treat the reshaped constant as a
        # another constant.
        out_var = eqn.outvars[0]
        inps = [jax_parameters[eqn.invars[0]]]
        jax_parameters[out_var] = eqn.primitive.bind(*inps, **eqn.params)
      else:
        # If it is a reshape on the pass of the network forward propagation, we
        # can ignore it as the forward evaluation code in sdp_verify handles the
        # reshaping itself
        continue
    elif eqn.primitive in (lax.dot_general_p,
                           lax.conv_general_dilated_p):
      if next_is_relu:
        raise ValueError('Unsupported architecture. Only supported networks are'
                         ' alternance of linear (convolutional/fully connected)'
                         ' and ReLU layers.')
      # Find the input which is a parameter.
      param_input = _get_const_input_arg(eqn)
      weight_params = jax_parameters[param_input]

      if eqn.primitive == lax.dot_general_p:
        bias_shape = weight_params.shape[1]
        scaling_shape = (-1, 1)
      else:
        bias_shape = (1, 1, 1, weight_params.shape[-1])
        # Based on the code in `fwd`, the dimension for the input channel is the
        # third one.
        scaling_shape = (1, 1, -1, 1)

      # Define the bias of the network, potentially incorporating existing
      # preprocessing steps
      bias = jnp.zeros(bias_shape)
      if centering is not None:
        inp_bias = jnp.zeros_like(example_input) + centering
        equivalent_bias = eqn.primitive.bind(inp_bias, weight_params,
                                             **eqn.params)
        bias += equivalent_bias
        centering = None
      if scaling is not None:
        scaling = jnp.reshape(scaling, scaling_shape)
        weight_params = weight_params * scaling
        scaling = None

      if eqn.primitive == lax.dot_general_p:
        layers.append((weight_params, bias))
      else:
        # The eval function of sdp_verify only handle stride equal
        # that are the same in all directions
        strides = eqn.params['window_strides']
        if not all(elt == strides[0] for elt in strides):
          raise ValueError('Different spatial strides unsupported.')
        # The forward code expect the bias to only correspond to one column.
        bias = jnp.reshape(bias[0, 0, 0, :], (1, 1, 1, -1))
        layers.append({
            'W': weight_params,
            'b': bias,
            'stride': strides[0],
            'padding': eqn.params['padding'],
        })
      next_is_relu = True
    elif eqn.primitive == lax.add_p:
      param_input = _get_const_input_arg(eqn)
      bias_params = jax_parameters[param_input]
      if not next_is_relu:
        raise ValueError('Unsupported architecture. Only supported networks are'
                         ' alternance of linear (convolutional/fully connected)'
                         ' and ReLU layers.')
      # This is an addition after a linear layer. Just fold it into the bias
      # of the previous layer.
      if isinstance(layers[-1], tuple):
        # Remove the last linear layer and include a version of it that includes
        # the bias term.
        weight, bias = layers.pop()
        layers.append((weight, bias + bias_params))
      else:
        layers[-1]['b'] = layers[-1]['b'] + bias_params
      # No need to update `next_is_relu` because it remains True
    elif eqn.primitive == lax.sub_p:
      if layers:
        # We handle this only in the case of preprocessing at the beginning of
        # the network.
        raise ValueError('Unsupported operation. sub is only supported as a'
                         'centering of the networks inputs.')
      # This appears potentially at the beginning of the network, during the
      # preprocessing of the inputs.
      centering = centering or 0.
      centering -= jax_parameters[_get_const_input_arg(eqn)]
    elif eqn.primitive == lax.div_p:
      if layers:
        # We handle this only in the case of preprocessing at the beginning of
        # the network.
        raise ValueError('Unsupported operation. div is only supported as a'
                         'rescaling of the networks inputs.')
      divide_scaling = jax_parameters[_get_const_input_arg(eqn)]
      # This appears during the preprocessing of the inputs of the networks.
      scaling = scaling or 1.0
      scaling /= divide_scaling
      # Rescale the centering if there is one.
      if centering is not None:
        centering /= divide_scaling
    elif eqn.primitive == lax.max_p:
      if ((not next_is_relu)
          or (not isinstance(eqn.invars[1], jax.core.Literal))
          or (eqn.invars[1].val != 0.0)):
        raise ValueError('Unsupported architecture. Only supported networks are'
                         ' alternance of linear (convolutional/fully connected)'
                         ' and ReLU layers.')
      # The ReLU are not denoted in the parameters dictionaries so no need to
      # add anything to the layers list.
      next_is_relu = False
    elif eqn.primitive == lax.broadcast_in_dim_p:
      # There might be broadcast of bias, we'll just store the original bias
      # where the broadcasted one should be.
      jax_parameters[eqn.outvars[0]] = jax_parameters[eqn.invars[0]]
    else:
      raise ValueError(f'Unsupported primitive {eqn.primitive}. The only '
                       'supported networks are alternance of linear '
                       '(convolutional / fully connected) and ReLU layers.')
  return layers


################## Bound prop ####################


def boundprop(params, bounds_in):
  """Compute IntervalBound for each layer."""
  layer_bounds = [bounds_in]
  for layer_params in params:
    lb_old = layer_bounds[-1].lb
    ub_old = layer_bounds[-1].ub

    if isinstance(layer_params, dict):
      center = (lb_old + ub_old) / 2.
      radius = (ub_old - lb_old) / 2.
      rad_layer_params = copy.deepcopy(layer_params)
      rad_layer_params['W'] = jnp.abs(layer_params['W'])
      rad_layer_params['b'] = jnp.zeros_like(layer_params['b'])
      act_c = fwd(center, layer_params)
      act_r = fwd(radius, rad_layer_params)
      lb = act_c - act_r
      ub = act_c + act_r
    else:
      if len(lb_old.shape) == 4:
        lb_old = lb_old.reshape((lb_old.shape[0], -1))
        ub_old = ub_old.reshape((ub_old.shape[0], -1))
      # TODO: Post-neurips. This logic can also be shared with above.
      W, b = layer_params

      lb = (jnp.matmul(lb_old, jnp.maximum(W, 0.)) +
            jnp.matmul(ub_old, jnp.minimum(W, 0.)) +
            b)
      ub = (jnp.matmul(ub_old, jnp.maximum(W, 0.)) +
            jnp.matmul(lb_old, jnp.minimum(W, 0.)) +
            b)

    layer_bounds.append(IntBound(lb_pre=lb,
                                 ub_pre=ub,
                                 lb=jnp.maximum(lb, 0.),
                                 ub=jnp.maximum(ub, 0.)))

  return layer_bounds


def init_bound(x, epsilon, input_bounds=(0., 1.), add_batch_dim=True):
  x = np.expand_dims(x, axis=0) if add_batch_dim else x
  lb_init = np.maximum(input_bounds[0], x - epsilon)
  ub_init = np.minimum(input_bounds[1], x + epsilon)
  return IntBound(lb=lb_init, ub=ub_init, lb_pre=None, ub_pre=None)


def ibp_bound_elided(verif_instance):
  assert len(verif_instance.bounds) == len(verif_instance.params) + 2
  obj, obj_const, final_bound = (
      verif_instance.obj, verif_instance.const, verif_instance.bounds[-2])
  ub = final_bound.ub.reshape(final_bound.ub.shape[0], -1)
  lb = final_bound.lb.reshape(final_bound.lb.shape[0], -1)
  obj_val = np.sum(np.maximum(obj, 0.) * ub +
                   np.minimum(obj, 0.) * lb)
  return float(obj_val + obj_const)


def ibp_bound_nonelided(verif_instance):
  assert len(verif_instance.bounds) == len(verif_instance.params) + 2
  obj_orig = verif_instance.obj_orig
  final_bound = verif_instance.bounds[-1]
  batch_size = final_bound.ub_pre.shape[0]
  ub = final_bound.ub_pre.reshape(batch_size, -1)
  lb = final_bound.lb_pre.reshape(batch_size, -1)
  obj_val = np.sum(np.maximum(obj_orig, 0.) * ub +
                   np.minimum(obj_orig, 0.) * lb)
  return float(obj_val)


################## Solver-agnostic Verification Instances ####################


class VerifInstanceTypes(enum.Enum):
  # `params` represent a network of repeated relu(Wx+b)
  # The final output also includes a relu activation, and `obj` composes
  # the final layer weights with the original objective
  MLP_ELIDED = 'mlp_elided'
  CNN_ELIDED = 'cnn_elided'


def make_relu_robust_verif_instance(
    params, bounds=None, target_label=1, label=2, input_bounds=None):
  """Make VerifInstance from network weights and input.

  Args:
    params: list of pairs of array-like objects [(W, b)], the weights and biases
      of a multi-layer perceptron.
    bounds: None, or a list of IntBound objects, of length len(params) + 1.
      The interval bounds for each layer.
    target_label: int, the adversary target
    label: int, the true label
    input_bounds: None, pair of floats, or pair of vectors with length matching
      input dimension. The image bounds e.g. (0, 1) or (0, 255).

  Returns:
    verif_instance: a VerifInstance object
  """
  assert bounds is None or len(bounds) == len(params) + 1
  if bounds is None:
    assert not any([isinstance(x, dict) for x in params])
    layer_sizes = mlp_layer_sizes(params)
  else:
    layer_sizes = layer_sizes_from_bounds(bounds)
  # Adversary maximizes objective - large when logit(target) > logit(label)
  if any([isinstance(x, dict) for x in params]):
    verif_type = VerifInstanceTypes.CNN_ELIDED
  else:
    verif_type = VerifInstanceTypes.MLP_ELIDED
  label_onehot = np.eye(int(layer_sizes[-1]))[label]
  target_onehot = np.eye(int(layer_sizes[-1]))[target_label]
  obj_orig = target_onehot - label_onehot
  w_fin, b_fin = params[-1]
  obj_bp = np.matmul(w_fin, obj_orig)
  const = np.vdot(obj_orig, b_fin)
  obj = np.reshape(obj_bp, (1, obj_bp.size))
  return _VerifInstance(
      params=params[:-1],
      params_full=params,
      input_bounds=input_bounds,
      bounds=bounds,
      obj=obj,
      obj_orig=obj_orig,
      const=const,
      type=verif_type)

make_nn_verif_instance = make_relu_robust_verif_instance  # alias

################## SDP Verification Instances ####################

# Dual variables correspond to:
#   lam: ReLU quadratic constraint: z^2 = z*(Wx)
#   nu: IBP quadratic constraint: x^2 <= (l+u)*x - l*u
#   nu_quad: IBP quadratic matrix constraint: (x_i - l_i)(x_j - u_j) <= 0
#   muminus: x'>=0
#   muminus2: Triangle linear Relu relaxation - u(Wx+b) - ul - (u-l)x' >= 0
#       where l = min(l, 0), u = max(u, 0)
#   muplus: x'>=Wx+b
DualVar = collections.namedtuple(
    'DualVar', ['lam', 'nu', 'nu_quad', 'muminus', 'muplus', 'muminus2'])
DualVarFin = collections.namedtuple('DualVarFin', ['nu', 'nu_quad'])
DEFAULT_DISABLED_DUAL_VARS = ('nu_quad', 'muminus2')
NECESSARY_DUAL_VARS = ('lam', 'muplus', 'muminus')


class DualVarTypes(enum.Enum):
  EQUALITY = 'equality'
  INEQUALITY = 'inequality'


def make_relu_network_lagrangian(dual_vars, params, bounds, obj):
  """Returns a function that computes the Lagrangian for a ReLU network.

  This function assumes `params` represent a feedforward ReLU network i.e.
  x_{i+1} = relu(W_i x_i + b_i). It defines the Lagrangian by applying the
  objective `obj` to the final layer activations, and encoding the Lagrangian
  terms for each of the constraints defining the ReLU network. It then returns
  this function.

  Args:
    dual_vars: A length L+1 list of dual variables at each layer
    params: A length L list of (W, b) pairs, elided network weights
    bounds: A length L+1 list of `IntBound`s, elided bounds at each layer
    obj: function, taking final layer activations as input

  Returns:
    Function that computes Lagrangian L(x) with fixed `dual_vars`.
  """
  layer_sizes = layer_sizes_from_bounds(bounds)

  def lagrangian(xs_list):
    """Computes Lagrangian L(x) with fixed `dual_vars`."""
    assert all([x.shape[0] == 1 for x in xs_list]), 'no batch mode support'

    lag = obj(xs_list[-1])
    for i in range(len(layer_sizes)):
      if i < len(params):
        y = fwd(xs_list[i], params[i])
        # Lagrangian for constraint x' * x' = x' * (Wx+b) where x'=ReLU(Wx+b)
        lag += (jnp.sum(dual_vars[i].lam * xs_list[i + 1] *
                        (y - xs_list[i + 1])))
        # Lagrangian for the constraint x'>=Wx+b
        lag += jnp.sum(dual_vars[i].muplus * (xs_list[i + 1] - y))
        if dual_vars[i].muminus2.shape:
          # Lagrangian for u(Wx+b) - ul - (u-l)x' >= 0, where
          # l = min(l, 0) and u = max(u, 0)
          raise NotImplementedError('dropped support for muminus2')

        # Lagrangian for the constraint x'>=0
        lag += jnp.sum(dual_vars[i].muminus * xs_list[i + 1])

      # Lagrangian for IBP constraint (x-l)(x-u) <= 0
      if dual_vars[i].nu.shape:
        lag += -jnp.sum(dual_vars[i].nu *
                        (xs_list[i] - bounds[i].lb) *(xs_list[i] - bounds[i].ub)
                        )
      if dual_vars[i].nu_quad.shape:
        # IBP quadratic matrix constraint: (x_i - l_i)(x_j - u_j) <= 0
        lag += -jnp.sum(dual_vars[i].nu_quad *
                        jnp.matmul((xs_list[i]-bounds[i].lb).T,
                                   xs_list[i]-bounds[i].ub))
    return lag
  return lagrangian


def relu_robustness_verif_instance_to_sdp(verif_instance):
  """Convert solver-agnostic VerifInstance to SdpDualVerifInstance."""
  assert verif_instance.type in [
      VerifInstanceTypes.MLP_ELIDED, VerifInstanceTypes.CNN_ELIDED]
  elided_bounds = verif_instance.bounds[:-1]
  dual_shapes, dual_types = get_dual_shapes_and_types(elided_bounds)
  def obj(x_final):
    out = jnp.sum(x_final * jnp.reshape(verif_instance.obj, x_final.shape))
    return out + verif_instance.const
  def make_inner_lagrangian(dual_vars):
    return make_relu_network_lagrangian(
        dual_vars, verif_instance.params, elided_bounds, obj)
  return SdpDualVerifInstance(
      make_inner_lagrangian=make_inner_lagrangian,
      bounds=elided_bounds,
      dual_shapes=dual_shapes,
      dual_types=dual_types)


def make_sdp_verif_instance(verif_instance):
  if isinstance(verif_instance, _AdvRobustnessVerifInstance):
    return relu_robustness_verif_instance_to_sdp(verif_instance)
  else:
    raise NotImplementedError('unrecognized verif_instance type')


def make_vae_sdp_verif_instance(params, data_x, bounds):
  """Make SdpDualVerifInstance for VAE reconstruction error spec."""
  elided_params = params[:-1]
  elided_bounds = bounds[:-1]
  dual_shapes, dual_types = get_dual_shapes_and_types(elided_bounds)
  def recon_loss(x_final):
    x_hat = predict_cnn(params[-1:], x_final).reshape(1, -1)
    return jnp.sum(jnp.square(data_x.reshape(x_hat.shape) - x_hat))
  def make_inner_lagrangian(dual_vars):
    return make_relu_network_lagrangian(
        dual_vars, elided_params, elided_bounds, recon_loss)
  return SdpDualVerifInstance(
      make_inner_lagrangian=make_inner_lagrangian,
      bounds=elided_bounds,
      dual_shapes=dual_shapes,
      dual_types=dual_types)


def make_vae_semantic_spec_params(x, vae_params, classifier_params):
  """Defines network f(z_noise) = classifier(reconstruct(x, z_noise))."""
  # Setup - encoder fwd pass
  encoder_params, decoder_params = vae_params
  encoder_mu_params = encoder_params[:-1]
  encoder_sigmasq_params = encoder_params[:-2] + [encoder_params[-1]]
  mu_z = predict_cnn(encoder_mu_params, x)
  log_sigmasq_z = predict_cnn(encoder_sigmasq_params, x)
  sigmasq_z = jnp.exp(log_sigmasq_z)
  # Combine the reparameterization with the first decoder layer
  # z0 = mu + sigma * z
  # z1 = jnp.dot(z0, W) + b
  #    = jnp.dot(mu + sigma * z, W) + b
  #    = jnp.dot(z, sigma * W) + [b + jnp.dot(mu, W)]
  assert isinstance(decoder_params[0], tuple)
  W0_orig, b0_orig = decoder_params[0]
  W0 = W0_orig * jnp.reshape(jnp.sqrt(sigmasq_z), (-1, 1))
  b0 = b0_orig + jnp.dot(mu_z, W0_orig)

  # Now the network is just concatenation of modified decoder + classifier
  # This is also applying a Relu to decoder output, but that's fine
  combined_params = [(W0, b0)] + decoder_params[1:] + classifier_params
  return combined_params


def get_dual_shapes_and_types(bounds_elided):
  """Get shapes and types of dual vars."""
  dual_shapes = []
  dual_types = []
  layer_sizes = layer_sizes_from_bounds(bounds_elided)
  for it in range(len(layer_sizes)):
    m = layer_sizes[it]
    m = [m] if isinstance(m, int) else list(m)
    if it < len(layer_sizes)-1:
      n = layer_sizes[it + 1]
      n = [n] if isinstance(n, int) else list(n)
      shapes = {
          'lam': [1] + n,
          'nu': [1] + m,
          'muminus': [1] + n,
          'muplus': [1] + n,
          'nu_quad': [], 'muminus2': [],
      }
      types = {
          'lam': DualVarTypes.EQUALITY,
          'nu': DualVarTypes.INEQUALITY,
          'muminus': DualVarTypes.INEQUALITY,
          'muplus': DualVarTypes.INEQUALITY,
          'nu_quad': DualVarTypes.INEQUALITY,
          'muminus2': DualVarTypes.INEQUALITY,
      }
      dual_shapes.append(DualVar(**{
          k: np.array(s) for k, s in shapes.items()}))
      dual_types.append(DualVar(**types))
    else:
      shapes = {'nu': [1] + m, 'nu_quad': []}
      types = {'nu': DualVarTypes.INEQUALITY,
               'nu_quad': DualVarTypes.INEQUALITY}
      dual_shapes.append(DualVarFin(**{
          k: np.array(s) for k, s in shapes.items()}))
      dual_types.append(DualVarFin(**types))

  # Add kappa
  N = sum([np.prod(np.array(i)) for i in layer_sizes])
  dual_shapes.append(np.array([1, N+1]))
  dual_types.append(DualVarTypes.INEQUALITY)
  return dual_shapes, dual_types


################### Image Preprocessing #######################


def preprocess_cifar(image, inception_preprocess=False, perturbation=False):
  """Proprocess images and perturbations."""
  if inception_preprocess:
    # Use 2x - 1 to get [-1, 1]-scaled images
    rescaled_devs = 0.5
    rescaled_means = 0.5
  else:
    rescaled_means = np.array([125.3, 123.0, 113.9]) / 255
    rescaled_devs = np.array([63.0, 62.1, 66.7]) / 255
  if perturbation:
    return image / rescaled_devs
  else:
    return (image - rescaled_means) / rescaled_devs


def preprocessed_cifar_eps_and_input_bounds(
    shape=(32, 32, 3), epsilon=2/255, inception_preprocess=False):
  """Get `epsilon` and `input_bounds`."""
  preprocess = functools.partial(
      preprocess_cifar, inception_preprocess=inception_preprocess)
  epsilon = preprocess(np.ones(shape)* epsilon, perturbation=True)
  input_bounds = (preprocess(np.zeros(shape)), preprocess(np.ones(shape)))
  return epsilon, input_bounds


################### Attacks #######################


def adv_objective(model_fn, x, label, target_label):
  logits = model_fn(x)
  if len(logits.shape) == 2:
    logits = logits[0]
  loss = logits[target_label] - logits[label]
  return jnp.sum(loss)


def fgsm_single(model_fn, x, label, target_label, epsilon, num_steps,
                step_size, input_bounds=(0., 1.)):
  """Same interface as l.d.r.adversarial.attacks, but no batch dim on x."""
  adv_loss = lambda *args, **kwargs: -adv_objective(*args, **kwargs)
  adv_loss_x = lambda x: adv_loss(model_fn, x, label, target_label)
  return pgd(adv_loss_x, x, epsilon, num_steps, step_size,
             input_bounds=input_bounds)


def untargeted_margin_loss(logits, labels):
  """Minimized by decreasing true score, and increasing second highest."""
  batch_size = logits.shape[0]
  num_classes = logits.shape[-1]
  label_logits = logits[jnp.arange(batch_size), labels]
  logit_mask = jax.nn.one_hot(labels, num_classes)
  inf = 1e5
  highest_logits = jnp.max(logits - inf * logit_mask, axis=-1)
  return label_logits - highest_logits


def pgd_default(model_fn, x, label, epsilon, num_steps, step_size,
                input_bounds=(0., 1.)):
  assert x.shape[0] == label.shape[0]
  adv_loss_x = lambda x: jnp.sum(untargeted_margin_loss(model_fn(x), label))
  return pgd(adv_loss_x, x, epsilon, num_steps, step_size,
             input_bounds=input_bounds)


def pgd(adv_loss, x_init, epsilon, num_steps, step_size, input_bounds=(0., 1.)):
  grad_adv_loss = jax.grad(adv_loss)
  x = x_init
  for _ in range(num_steps):
    grad_x = grad_adv_loss(x)
    x -= jnp.sign(grad_x) * step_size
    x = jnp.clip(x, x_init - epsilon, x_init + epsilon)
    x = jnp.clip(x, input_bounds[0], input_bounds[1])
  return x


################ Optimizers ##################


def scale_by_variable_opt(multipliers):
  """Custom learning rates for different variables.

  Args:
    multipliers: a pytree, with the same structure as `params`. Each leaf can
      be either a float, or an array shape-compatible with the corresponding
      `params` element. These multiply the learning rate for each leaf.

  Returns:
    optax.GradientTransformation optimizer
  """

  def init_fn(params):
    params_struct = jax.tree_map(lambda _: None, params)
    multipliers_struct = jax.tree_map(lambda _: None, multipliers)
    assert params_struct == multipliers_struct, (
        'multipliers should have same struct as params')
    return None

  def update_fn(updates, _, params=None):
    del params  # Unused.
    scaled_updates = jax.tree_multimap(lambda a, g: a * g, multipliers, updates)
    return scaled_updates, None

  return optax.GradientTransformation(init_fn, update_fn)


################ Pytrees / Misc ##################


def flatten(pytree, backend=np):
  """Take pytree of arrays, then flatten tree, flatten arrays, concatenate."""
  seq = tree.flatten(pytree)
  seq_flat = [backend.reshape(x, -1) for x in seq]
  return backend.concatenate(seq_flat)


def unflatten_like(a, pytree):
  """Take 1-D array produced by flatten() and unflatten like pytree."""
  seq = tree.flatten(pytree)
  seq_sizes = [np.reshape(x, -1).shape for x in seq]
  starts = [0] + list(np.cumsum(seq_sizes))
  a_seq_flat = [a[starts[i]:starts[i+1]] for i in range(len(starts)-1)]
  a_seq = [np.reshape(x1, x2.shape) for x1, x2 in zip(a_seq_flat, seq)]
  return tree.unflatten_as(pytree, a_seq)


def structure_like(tree1, tree2):
  # pylint: disable=g-doc-args, g-doc-return-or-yield
  """Makes tree1 have same structure as tree2."""
  flat_paths1 = tree.flatten_with_path(tree.map_structure(lambda x: 0, tree1))
  flat_paths2 = tree.flatten_with_path(tree.map_structure(lambda x: 0, tree2))
  assert list(sorted(flat_paths1)) == list(sorted(flat_paths2)), (
      'paths of tree1 and tree2 do not match')
  indices = [flat_paths1.index(path) for path in flat_paths2]
  flat_tree1 = tree.flatten(tree1)
  reordered_flat_tree1 = [flat_tree1[i] for i in indices]
  return tree.unflatten_as(tree2, reordered_flat_tree1)
