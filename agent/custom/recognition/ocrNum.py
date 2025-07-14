from maa.agent.agent_server import AgentServer
from maa.custom_recognition  import CustomRecognition
from maa.context import Context
from utils import logger


@AgentServer.custom_recognition("OCRNum")
class OCRNum(CustomRecognition):
    def analyze(
         self,
         context: Context,
         argv: CustomRecognition.AnalyzeArg,
     ) -> CustomRecognition.AnalyzeResult:
        """
        获取活跃度并判断
        """
        logger.info("OCRNum")
        image1 = context.tasker.controller.post_screencap().wait().get()
        recoNum =  context.run_recognition(
            "识别活跃度",
            image1,
            pipeline_override={
                "识别活跃度":{"roi" : [311,500,917,152],
                              "expected":[""],
                              "recognition": "OCR"
                            }
                }

            )
        logger.info(f"识别结果: {recoNum}")
        if not recoNum or not recoNum.all_results:
                logger.info("没有识别到活跃度")

                return CustomRecognition.AnalyzeResult(box=(0,0,0,0),detail="没有识别到活跃度")
        for res in recoNum.all_results:
            # num = int(res.text)
            num = OCRNum.convert_to_int(res.text)
            if num >= 50:
                context.run_task("活动-运镖-点击日常活动")
                return CustomRecognition.AnalyzeResult(box=(0,0,0,0),detail="活跃度大于50")
            else:
                context.run_task("panduan_zhujiemian")
                return CustomRecognition.AnalyzeResult(box=(0,0,0,0),detail="活跃度小于50,任务结束")

    def convert_to_int(s):
        try:
            num = int(s)
            logger.info("活跃度为: %s", num)
            return num
        except ValueError:
            logger.info("识别活跃度错误", s)
            return CustomRecognition.AnalyzeResult(box=(0,0,0,0),detail="识别活跃度错误")
