from __future__ import absolute_import

from oneflow.python.oneflow_export import oneflow_export
import oneflow.python.ops.user_op_builder as user_op_builder
import oneflow.python.framework.id_util as id_util
import oneflow.python.framework.distribute as distribute_util
import oneflow.python.framework.hob as hob
import oneflow.python.lib.core.enable_if as enable_if

import oneflow as flow


@oneflow_export("math.two_stage_reduce_max")
def api_two_stage_reduce_max(x, axis=None, keepdims=False, name=None):
    func = enable_if.unique([two_stage_reduce_max])
    return func(x, axis=axis, keepdims=keepdims, name=name)


@enable_if.condition(hob.in_global_mode & ~hob.eager_execution_enabled)
def two_stage_reduce_max(x, axis=None, keepdims=False, name=None):
    name = name if name is not None else id_util.UniqueStr("ReduceMax_")
    return two_stage_reduce(x, axis, keepdims, "reduce_max", name)


@oneflow_export("math.two_stage_reduce_min")
def api_two_stage_reduce_min(x, axis=None, keepdims=False, name=None):
    func = enable_if.unique([two_stage_reduce_min])
    return func(x, axis=axis, keepdims=keepdims, name=name)


@enable_if.condition(hob.in_global_mode & ~hob.eager_execution_enabled)
def two_stage_reduce_min(x, axis=None, keepdims=False, name=None):
    name = name if name is not None else id_util.UniqueStr("ReduceMin_")
    return two_stage_reduce(x, axis, keepdims, "reduce_min", name)


def two_stage_reduce(x, axis=None, keepdims=False, op_type_name=None, name=None):

    assert check_x_dictribute(x, axis)
    axis = _check_axis(axis, x.shape)

    device_stage_out_list = []
    device_stage_count_list = []
    distribute_axis = x.distribute.axis
    x_list = flow.advanced.distribute_split(x, axis=distribute_axis)
    current_placement_scope = flow.placement.current_scope()
    device_tag = current_placement_scope.default_device_tag
    parallel_id = 0
    for (
        machine_id,
        device_ids,
    ) in current_placement_scope.machine_id2device_id_list.items():
        for device_id in device_ids:
            with flow.fixed_placement(
                device_tag, str(machine_id) + ":" + str(device_id)
            ):
                device_stage_out, device_stage_count = reduce_device_stage(
                    x_list[parallel_id],
                    axis,
                    op_type_name + "_device_stage",
                    name + "_device_stage" + str(parallel_id),
                )
                device_stage_out_list.append(device_stage_out)
                device_stage_count_list.append(device_stage_count)
                parallel_id += 1
    device_stage_out = flow.advanced.distribute_concat(
        device_stage_out_list, axis=distribute_axis
    )
    device_stage_count = flow.advanced.distribute_concat(
        device_stage_count_list, axis=distribute_axis
    )

    device_stage_out = device_stage_out.with_distribute(flow.distribute.broadcast())
    device_stage_count = device_stage_count.with_distribute(flow.distribute.broadcast())

    out = reduce_global_stage(
        device_stage_out,
        device_stage_count,
        axis,
        keepdims,
        op_type_name + "_global_stage",
        name + "_global_stage",
    )
    return out


def reduce_device_stage(x, axis, op_name, name):
    out, mask, count = (
        flow.user_op_builder(name)
        .Op(op_name)
        .Input("in", [x])
        .Output("out")
        .Output("mask")
        .Output("count")
        .Attr("axis", axis, "AttrTypeListInt32")
        .Build()
        .InferAndTryRun()
        .RemoteBlobList()
    )
    return out, count


def reduce_global_stage(x, device_count, axis, keepdims, op_name, name):
    out, mask = (
        flow.user_op_builder(name)
        .Op(op_name)
        .Input("in", [x])
        .Input("device_count", [device_count])
        .Output("out")
        .Output("mask")
        .Attr("axis", axis, "AttrTypeListInt32")
        .Attr("keepdims", keepdims, "AttrTypeBool")
        .Build()
        .InferAndTryRun()
        .RemoteBlobList()
    )
    return out


def _check_axis(axis, shape):
    if axis is None:
        axis = list(range(len(shape)))

    if isinstance(axis, int):
        axis = [axis]

    assert isinstance(axis, (list, tuple)), "Invalid axis {}".format(axis)
    for x in axis:
        if x < 0:
            x += len(shape)
        assert x >= 0 and x < len(shape), "Invalid axis {}".format(axis)

    return axis


def check_x_dictribute(x, axis):
    for i in axis:
        if x.distribute is distribute_util.split(i):
            return True
    return False
