from __future__ import absolute_import

import os

import oneflow as flow
import oneflow.core.operator.op_conf_pb2 as op_conf_util
import oneflow.core.register.logical_blob_id_pb2 as logical_blob_id_util
import oneflow.python.framework.interpret_util as interpret_util
import oneflow.python.framework.id_util as id_util
import oneflow.python.framework.remote_blob as remote_blob_util
import oneflow.python.ops.user_op_builder as user_op_builder
from oneflow.python.oneflow_export import oneflow_export


def build_unary_elemwise_math_op(math_op, x, name=None):
    if name is None:
        name = id_util.UniqueStr(math_op + "_")
    return (
        flow.user_op_builder(name)
        .Op(math_op)
        .Input("x", [x])
        .Output("y")
        .Build()
        .InferAndTryRun()
        .RemoteBlobList()[0]
    )


@oneflow_export("math.abs")
def abs(x, name=None):
    return build_unary_elemwise_math_op("abs", x, name)


@oneflow_export("math.acos")
def acos(x, name=None):
    return build_unary_elemwise_math_op("acos", x, name)


@oneflow_export("math.acosh")
def acosh(x, name=None):
    return build_unary_elemwise_math_op("acosh", x, name)


@oneflow_export("math.asin")
def asin(x, name=None):
    return build_unary_elemwise_math_op("asin", x, name)


@oneflow_export("math.asinh")
def asinh(x, name=None):
    return build_unary_elemwise_math_op("asinh", x, name)


@oneflow_export("math.atan")
def atan(x, name=None):
    return build_unary_elemwise_math_op("atan", x, name)


@oneflow_export("math.atanh")
def atanh(x, name=None):
    return build_unary_elemwise_math_op("atanh", x, name)


@oneflow_export("math.ceil")
def ceil(x, name=None):
    return build_unary_elemwise_math_op("ceil", x, name)


@oneflow_export("math.cos")
def cos(x, name=None):
    return build_unary_elemwise_math_op("cos", x, name)


@oneflow_export("math.cosh")
def cosh(x, name=None):
    return build_unary_elemwise_math_op("cosh", x, name)


@oneflow_export("math.erf")
def erf(x, name=None):
    return build_unary_elemwise_math_op("erf", x, name)


@oneflow_export("math.erfc")
def erfc(x, name=None):
    return build_unary_elemwise_math_op("erfc", x, name)


@oneflow_export("math.exp")
def exp(x, name=None):
    return build_unary_elemwise_math_op("exp", x, name)


@oneflow_export("math.expm1")
def expm1(x, name=None):
    return build_unary_elemwise_math_op("expm1", x, name)


@oneflow_export("math.floor")
def floor(x, name=None):
    return build_unary_elemwise_math_op("floor", x, name)


@oneflow_export("math.lgamma")
def lgamma(x, name=None):
    return build_unary_elemwise_math_op("lgamma", x, name)


@oneflow_export("math.log")
def log(x, name=None):
    return build_unary_elemwise_math_op("log", x, name)


@oneflow_export("math.log1p")
def log1p(x, name=None):
    return build_unary_elemwise_math_op("log1p", x, name)


@oneflow_export("math.log_sigmoid")
def log_sigmoid(x, name=None):
    return build_unary_elemwise_math_op("log_sigmoid", x, name)


@oneflow_export("math.negative")
def negative(x, name=None):
    return build_unary_elemwise_math_op("negative", x, name)


@oneflow_export("math.reciprocal")
def reciprocal(x, name=None):
    return build_unary_elemwise_math_op("reciprocal", x, name)


@oneflow_export("math.reciprocal_no_nan")
def reciprocal_no_nan(x, name=None):
    return build_unary_elemwise_math_op("reciprocal_no_nan", x, name)


@oneflow_export("math.rint")
def rint(x, name=None):
    return build_unary_elemwise_math_op("rint", x, name)


@oneflow_export("math.round")
def round(x, name=None):
    return build_unary_elemwise_math_op("round", x, name)


@oneflow_export("math.rsqrt")
def rsqrt(x, name=None):
    return build_unary_elemwise_math_op("rsqrt", x, name)


@oneflow_export("math.sigmoid_v2")
def sigmoid_v2(x, name=None):
    return build_unary_elemwise_math_op("sigmoid_v2", x, name)


@oneflow_export("math.sign")
def sign(x, name=None):
    return build_unary_elemwise_math_op("sign", x, name)


@oneflow_export("math.sin")
def sin(x, name=None):
    return build_unary_elemwise_math_op("sin", x, name)


@oneflow_export("math.sinh")
def sinh(x, name=None):
    return build_unary_elemwise_math_op("sinh", x, name)


@oneflow_export("math.softplus")
def softplus(x, name=None):
    return build_unary_elemwise_math_op("softplus", x, name)


@oneflow_export("math.sqrt")
def sqrt(x, name=None):
    return build_unary_elemwise_math_op("sqrt", x, name)


@oneflow_export("math.square")
def square(x, name=None):
    return build_unary_elemwise_math_op("square", x, name)


@oneflow_export("math.tan")
def tan(x, name=None):
    return build_unary_elemwise_math_op("tan", x, name)


@oneflow_export("math.tanh_v2")
def tanh_v2(x, name=None):
    return build_unary_elemwise_math_op("tanh_v2", x, name)
