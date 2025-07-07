import os
import json
from datetime import datetime

from PIL import Image
from maa.agent.agent_server import AgentServer
from maa.custom_recognition  import CustomRecognition
from maa.context import Context

from utils import logger

@AgentServer.custom_recognition("sanjie_reco")
class sanjie_reco(CustomRecognition):
    def analyze(
         self,
         context: Context,
         argv: CustomRecognition.AnalyzeArg,
     ) -> CustomRecognition.AnalyzeResult:
        logger.info("进入到sjq_reco")
        m= context.run_recognition("福利",argv.image,pipeline_override={"福利":{"roi":[6,134,57,46]}}),
        print(m)
        logger.info("进入到sjq")
        return CustomRecognition.AnalyzeResult(box=(6,134,57,46),detail="福利")
        # reco_detail = context.run_recognition(
        #     "福利",  # 假设这是用于识别"福利"文字的识别器名称
        #     argv.image,
        #     pipeline_override={"福利": {"roi": [6,134,57,46]}},  # 示例ROI区域
        # )

        # # 根据reco_detail中的信息判断是否找到了"福利"文字
        # if "福利" in reco_detail.detail:
        #     # 如果找到了"福利"文字，计算中心点并执行点击
        #     box = reco_detail.box  # 假设box为(x_min, y_min, x_max, y_max)
        #     center_x = (box[0] + box[2]) // 2
        #     center_y = (box[1] + box[3]) // 2

        #     click_job = context.tasker.controller.post_click(center_x, center_y)
        #     click_job.wait()  # 等待点击操作完成

        #     # 返回分析结果
        #     return CustomRecognition.AnalyzeResult(
        #         box=box, detail="Found '福利' and clicked!"
        #     )
        # else:
        #     # 如果没有找到"福利"文字，返回相应的结果
        #     return CustomRecognition.AnalyzeResult(
        #         box=(0, 0, 0, 0), detail="Did not find '福利'."
        #     )