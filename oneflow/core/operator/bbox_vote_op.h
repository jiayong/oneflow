#ifndef ONEFLOW_CORE_OPERATOR_BBOX_VOTE_OP_H_
#define ONEFLOW_CORE_OPERATOR_BBOX_VOTE_OP_H_

#include "oneflow/core/operator/operator.h"

namespace oneflow {

class BboxVoteOp final : public Operator {
 public:
  OF_DISALLOW_COPY_AND_MOVE(BboxVoteOp);
  BboxVoteOp() = default;
  ~BboxVoteOp() = default;

  void InitFromOpConf() override;
  const PbMessage& GetCustomizedConf() const override;
  void InferBlobDescs(std::function<BlobDesc*(const std::string&)> GetBlobDesc4BnInOp,
                      const ParallelContext* parallel_ctx) const override;
};

}  // namespace oneflow

#endif  // ONEFLOW_CORE_OPERATOR_BBOX_VOTE_OP_H_
