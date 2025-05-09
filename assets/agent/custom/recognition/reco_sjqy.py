import os
import json
from datetime import datetime

from PIL import Image
from maa.agent.agent_server import AgentServer
from maa.custom_recognition  import CustomRecognition
from maa.context import Context
from fuzzywuzzy import fuzz, process
from typing import Dict, List, Tuple
from utils import logger
import json
import time


@AgentServer.custom_recognition("reco2")
class reco2_sjqy(CustomRecognition):
    def analyze(
         self,
         context: Context,
         argv: CustomRecognition.AnalyzeArg,
     ) -> CustomRecognition.AnalyzeResult:
        logger.info("进入reco2_sjqy")
        return CustomRecognition.AnalyzeResult(box=(6,134,57,46),detail="福利")

        # reco_detail = context.run_recognition(
        #     "福利",  # 假设这是用于识别"福利"文字的识别器名称
        #     argv.image,
        #     pipeline_override={"福利": {"roi": [6,134,57,46]}},  # 示例ROI区域
        # )
        # logger.info(reco_detail)
        # # 根据reco_detail中的信息判断是否找到了"福利"文字
        # if "福利" in reco_detail.detail:
        #     # 如果找到了"福利"文字，计算中心点并执行点击
        #     box = reco_detail.box  # 假设box为(x_min, y_min, x_max, y_max)
        #     center_x = box[0] + box[2] // 2
        #     center_y = box[1] + box[3] // 2 

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

@AgentServer.custom_recognition("reco3")
class reco2_sjqy(CustomRecognition):
    def analyze(
         self,
         context: Context,
         argv: CustomRecognition.AnalyzeArg,
     ) -> CustomRecognition.AnalyzeResult:
        logger.info("进入reco3")

        """
        测试，custom_recognition
        1.识别文字“福利”,box=(6,134,57,46)
        2.发送click
        """
        reco_detail = context.run_recognition(
            "福利",
            argv.image,
            pipeline_override={"福利": {"roi": [6,134,57,46],
                                        "expected":["福利"],
                                        "recognition": "OCR"
                                      }}
            )
        if "福利" in reco_detail.all_results[0].text:
            # 如果找到了"福利"文字，计算中心点并执行点击
            box = reco_detail.box  # 假设box为(x, y, w, h)
            center_x = box[0] + box[2] // 2
            center_y = box[1] + box[3] // 2 

            click_job = context.tasker.controller.post_click(center_x, center_y)
            click_job.wait()  # 等待点击操作完成

        logger.info(reco_detail.all_results[0].text)

        # logger.info(argv.image)
        # print(img)
        # box=(6,134,57,46),detail="福利"
        return CustomRecognition.AnalyzeResult(box=(6,134,57,46),detail="福利")
    


        # # image array(BGR)
        # screen_array = context.tasker.controller.post_screencap().wait().get()
        # # BGR2RGB
        # if len(screen_array.shape) == 3 and screen_array.shape[2] == 3:
        #     rgb_array = screen_array[:, :, ::-1]
        # else:
        #     rgb_array = screen_array
        #     logger.warning("当前截图并非三通道")

        # img = Image.fromarray(rgb_array)
        # # img.save(f"./1.png")
        # img = context.tasker.controller.cached_image

# 读取JSON文件
# def load_question_bank(file_path: str) -> Dict[str, List[str]]:
#     """加载问题库JSON文件"""
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         print(f"错误：文件 {file_path} 未找到")
#         return {}
#     except json.JSONDecodeError:
#         print(f"错误：文件 {file_path} 不是有效的JSON格式")
#         return {}

# # 加载问题库数据
# rapath = f'D:\\codeWork\\Maa_MHXY_MG\\assets\\agent\\custom\\recognition\\question_bank.json'
# question_bank = load_question_bank(rapath)
# logger.info(f"问题库数据: {question_bank}")


def fuzzy_search_question_bank(
    keyword: str, 
    bank_data: Dict[str, List[str]], 
    cutoff: int = 80
) -> Tuple[str, int]:
    """模糊搜索问题库
    
    参数:
        keyword: 搜索关键词
        bank_data: 问题库数据
        cutoff: 相似度阈值(0-100)
        
    返回:
        (格式化结果字符串, 结果数量)
    """
    results = set()  # 使用集合避免重复
    keyword_lower = keyword.lower()
    
    # 对问题进行模糊匹配
    questions = list(bank_data.keys())
    question_matches = process.extract(
        keyword_lower, 
        questions, 
        scorer=fuzz.partial_ratio, 
        limit=len(questions)
    )
    
    for question, score in question_matches:
        if score >= cutoff:
            results.update(bank_data[question])

    # 对答案进行模糊匹配
    for answers in bank_data.values():
        for answer in answers:
            answer_score = fuzz.partial_ratio(keyword_lower, answer.lower())
            if answer_score >= cutoff:
                results.add(answer)
    
    formatted_results = json.dumps(list(results), ensure_ascii=False)
    return formatted_results, len(results)

@AgentServer.custom_recognition("sjqy_tiku")
class sjqy_tiku(CustomRecognition):

    def analyze(
         self,
         context: Context,
         argv: CustomRecognition.AnalyzeArg,
     ) -> CustomRecognition.AnalyzeResult:
        logger.info("进入三界奇缘答题agent")
        #识别三界奇缘题目
        reco_detail = context.run_recognition(
            "三界奇缘题目",
            argv.image,
            pipeline_override={"三界奇缘题目": {"roi" : [477,68,613,47],
                                                "expected":[""],
                                                "recognition": "OCR"
                                                }
                                }
            )
        logger.info(reco_detail)
        for res in reco_detail.all_results:#识别的结果在题库中搜索问题答案
            text =res.text
            # logger.info(len(text))
            excluded_texts = {#排除的文本
                '第1题：', '第2题：', '第3题：', '第4题：', '第5题：', 
                '第6题：', '第7题：', '第8题：', '第9题：', '第10题：', 
                '(1/3)', '(2/3)', '(3/3)', '(1/2)', '(2/2)', '(1/1)'
            }
            if text not in excluded_texts:   
                logger.info(f"问题为:"+text)
                # 在题库中搜索答案
                results_value, results_len = fuzzy_search_question_bank(text, question_bank)
                logger.info(f"搜索题库返回结果:"+results_value)
                logger.info(f"搜索题库返回结果个数:"+str(results_len))
                # if results_len:#搜索到结果进入循环，否则直接点击第一个
                #     for i in range(results_len):#按照答案个数循环ocr并点击
                new_context = context.clone()
                new_reco_detail = new_context.run_recognition(
                                "三界奇缘答案位置",
                                argv.image,
                                pipeline_override={"三界奇缘答案位置": {"roi" : [475,340,613,49],
                                                                    "expected":results_value,
                                                                    "recognition": "OCR"
                                                                    }
                                                    }
                                )
                # logger.info("new_reco_detail为：{new_reco_detail}")
                # logger.info(new_reco_detail.box)
                if new_reco_detail:
                    box = new_reco_detail.box  # 假设box为(x, y, w, h)
                    center_x = box[0] + box[2] // 2
                    center_y = box[1] + box[3] // 2 
                    time.sleep(2)
                    click_job = new_context.tasker.controller.post_click(center_x, center_y)
                    click_job.wait()  # 等待点击操作完成
                    time.sleep(2)
                        # else:
                        #     context.tasker.controller.post_click(500, 344).wait()
                        #     time.sleep(1.5)
                # else:
                    # context.tasker.controller.post_click(500, 344).wait()
                    # time.sleep(1.5)
                    # return CustomRecognition.AnalyzeResult(box=reco_detail.box,detail="") 
           
        # logger.info(reco_detail.all_results[0].text)
        # logger.info(reco_detail)
        return CustomRecognition.AnalyzeResult(box=reco_detail.box,detail="")



question_bank ={"出2个仙族主角":["龙太子","羽灵神"],
                
    "以下谁是玉皇大帝的外甥？": [
        "二郎神"
    ],
    "以下谁有可能是骨精灵的师父？": [
        "大大王",
        "地藏王"
    ],
    "以下谁是小柔的意中人？": [
        "鲛将军"
    ],
    "以下谁奉命行事惩罚卷帘？": [
        "天兵飞剑"
    ],
    "以下哪个主角可以拜入须弥海？": [
        "越星河"
    ],
    "以下哪个伙伴精通“失心符”技能？": [
        "太白金星"
    ],
    "以下哪个妖怪曾让如来佛祖吃了苦头？": [
        "蝎子精"
    ],
    "以下谁是宝象国公主？": [
        "百花羞"
    ],
    "以下谁吃过人？": [
        "翻天怪",
        "李彪"
    ],
    "以下哪个妖怪是被昂日星官杀死的？": [
        "蝎子精"
    ],
    "以下谁收留了婴孩时期的玄奘？": [
        "法明长老"
    ],
    "以下哪些师父的弟子会恢复气血技能？": [
        "观音姐姐",
        "空度禅师",
        "地藏王"
    ],
    "以下哪个伙伴的法术会附加护盾？": [
        "杏林仙"
    ],
    "以下哪个伙伴拥有翅膀？": [
        "大鹏王"
    ],
    "以下谁有炼丹炉？": [
        "太上老君"
    ],
    "以下哪个伙伴可以攻击隐身单位？": [
        "九灵元圣"
    ],
    "以下谁与猪八戒有爱情纠葛？": [
        "嫦娥仙子",
        "卵二姐",
        "高翠兰"
    ],
    "以下谁是罗仟仟心之所属？": [
        "吴举人"
    ],
    "以下谁又摔碎了你复原好的琉璃盏？": [
        "王母娘娘"
    ],
    "以下谁的鬼魂曾进皇宫索命唐王？": [
        "泾河龙王"
    ],
    "以下谁使用环圈作为武器？": [
        "飞燕女"
    ],
    "以下谁和孙悟空是结拜兄弟？": [
        "镇元子"
    ],
    "以下哪只召唤灵足下生花？": [
        "芙蓉仙子"
    ],
    "以下哪个伙伴每次出手有概率召唤印记？": [
        "铁扇公主"
    ],
    "以下哪个妖怪曾经战胜过孙悟空？": [
        "红孩儿"
    ],
    "以下哪种召唤灵天生可能携带力劈华山？": [
        "巨灵神将"
    ],
    "以下哪个人物不属于助战伙伴？": [
        "程咬金"
    ],
    "以下谁云游四方得了重病？": [
        "法明长老"
    ],
    "以下哪个是人族角色？": [
        "越星河"
    ],
    "以下哪个是魔族角色？": [
        "巨魔王",
        "喵千岁"
    ],
    "以下谁使用斧钺作为武器？": [
        "虎头怪"
    ],
    "以下谁被称作地仙之祖？": [
        "镇元子"
    ],
    "以下谁有可能是杀破狼的师父？": [
        "大大王",
        "地藏王"
    ],
    "以下谁的武器是斧子？": [
        "强盗头子",
        "程咬金"
    ],
    "以下谁有3只眼睛？": [
        "二郎神"
    ],
    "以下谁使用长戈作为武器？": [
        "长孙靖"
    ],
    "以下谁是太乙真人的徒弟？": [
        "哪吒"
    ],
    "以下谁不曾是天蓬的情障？": [
        "飞霞",
        "白姑娘"
    ],
    "以下谁是金蝉子转世？": [
        "唐僧"
    ],
    "以下谁被称作如来佛祖的舅舅？": [
        "大鹏王"
    ],
    "以下谁有可能是漠少君的师父？": [
        "程咬金",
        "菩提祖师"
    ],
    "以下谁会三十六变？": [
        "猪八戒"
    ],
    "以下哪位伙伴会有几率在回合结束后变身？": [
        "北海龙王"
    ],
    "以下哪些师父的弟子会复活同伴类技能？": [
        "空度禅师，观音姐姐"
    ],
    "以下哪个伙伴拥有“魅惑”技能？": [
        "玉面狐狸"
    ],
    "以下谁拥有尾巴？": [
        "狐美人"
    ],
    "以下谁使用长刀作为武器": [
        "巨魔王"
    ],
    "以下哪只召唤灵的初始变异色是白色？": [
        "蟹将"
    ],
    "以下谁使用弓作为武器？": [
        "杀破狼"
    ],
    "以下哪个是仙族角色？": [
        "舞天姬",
        "神天兵",
        "梦灵珑"
    ],
    "以下哪些师父的弟子会群体增益类技能？": [
        "空度禅师","观音姐姐","地藏王"
    ],
    "以下谁使用剑作为武器？": [
        "星宿神君","小白龙"
    ],
    "以下谁使用弯刀作为武器？": [
        "漠少君"
    ],
    "以下谁有可能是羽灵神的师父？": [
        "东海龙王","观音姐姐"
    ],
    "以下谁不能拜入月宫门派？": [
        "长孙靖"
    ],
    "以下哪种召唤灵天生没有特殊技能？": [
        "吸血鬼"
    ],
    "以下谁曾大闹袁守城儿子的婚礼？": [
        "泾河龙王"
    ],
    "以下谁是狮驼国国王？": [
        "三大王"
    ],
    "以下谁会72变？": [
        "二郎神，孙悟空"
    ],
    "以下哪个伙伴变身后拥有不同的战斗特性？": [
        "北海龙王"
    ],
    "以下哪个妖怪住在积雷山魔云洞？": [
        "玉面狐狸"
    ],
    "以下谁有可能是英女侠的师父": [
        "程咬金，菩提祖师"
    ],
    "以下谁使用枪作为武器": [
        "龙太子，哪吒"
    ],
    "以下谁是托塔天王的义女？": [
        "地涌夫人"
    ],
    "以下谁是莲花之身？": [
        "哪吒"
    ],
    "以下谁使用魔棒作为武器": [
        "玄彩娥"
    ],
    "以下谁有可能是玄彩娥的师父？": [
        "月灵，观音姐姐"
    ],
    "以下哪个伙伴会使用“龙腾”技能": [
        "北海龙子"
    ],
    "以下哪个召唤灵拥有翅膀？": [
        "吸血鬼"
    ],
    "以下谁精通三昧真火？": [
        "牛魔王，红孩儿"
    ],
    "以下谁是狮子怪？": [
        "九元圣灵"
    ],
    "以下哪个伙伴会使用“潜灵养性”技能？": [
        "小白龙"
    ],
    "找出2个勾魂使者。": [
        "黑无常",
        "白无常"
    ],
    "找出2个孙悟空的师父？": [
        "唐僧",
        "菩提老祖"
    ],
    "找出牛魔王一家人。": [
        "牛魔王",
        "铁扇公主",
        "红孩儿"
    ],
    "找出2个治疗型三界群雄。": [
        "唐僧",
        "观音菩萨"
    ],
    "找出3个龙宫侍卫？": [
        "虾兵",
        "蟹将",
        "龟千岁"
    ],
    "找出手游中的3个门派师父。": [
        "超凡孙悟空",
        "菩提祖师",
        "程咬金"
    ],
    "找出2个魔族主角。": [
        "巨魔王",
        "喵千岁"
    ],
    "找出2个道家弟子。": [
        "牛大胆",
        "道童"
    ],
    "找出3只海底迷宫的召唤灵": [
        "鲛将军",
        "蟹将",
        "龟丞相",
        "龙女，蚌仙子，虾兵"
    ],
    "找出3个稀有召唤灵": [
        "鬼将",
        "御风童子",
        "芙蓉仙子"
    ],
    "找出3只瑶池珍兽。": [
        "芙蓉仙子",
        "雾中仙",
        "猴小仙",
        "凤凰仙子",
        "蛟龙",
        "啸天虎"
    ],
    "找出3个常驻花果山的角色？": [
        "孙悟空",
        "芭将军",
        "孙小圣"
    ],
    "找出3个孙悟空的结拜兄弟": [
        "牛魔王",
        "蛟魔王",
        "鹏魔王"
    ],
    "找出2个太上老君的道童变化的妖怪": [
        "金角大王",
        "银角大王"
    ],
    "找出2个人族角色": [
        "英女侠",
        "越星河"
    ],
    "找出3个拥有翅膀的主角": [
        "玄彩娥",
        "骨精灵",
        "羽灵神"
    ],
    "找出常驻傲来渔港的3个角色。": [
        "偷偷怪",
        "小紫",
        "神机道长"
    ],
    "找出平顶山的妖怪": [
        "金角大王，银角大王"
    ],
    "找出2个辅助型三界群雄": [
        "地藏菩萨，蝎子精"
    ],
    "找出3个天宫神将": [
        "二郎神，哪吒，李靖"
    ],
    "找出麒麟山的2个妖怪": [
        "赛太岁，有来有去"
    ],
    "找出3只瑶池珍兽": [
        "蟠桃童子，天兵，凤凰仙子"
    ],
    "找出3个生活在地府的角色": [
        "千年僵尸，孤魂野鬼，吸血鬼"
    ],
    "找出2个法攻型三界群雄": [
        "西海龙王，小白龙"
    ],
    "找出3个大唐官员": [
        "魏征，程咬金，马副将"
    ],
    "找出3个常驻长安城的角色": [
        "钟馗，张老财，吴举人"
    ],
    "找出3只地府恶鬼": [
        "夜叉，鬼将，幽莹娃娃",
        "吸血鬼，孤魂野鬼，千年僵尸"
    ],
    "找出2个佛家弟子": [
        "法明长老，小和尚"
    ],
    "找出3个常驻长寿村的角色": [
        "毛驴张，卵二姐，陆萧然"
    ],
    "找出3个一国之主": [
        "女儿国王，朱紫国王，三大王"
    ],
    "找出3只生活在大雁塔的召唤灵": [
        "野猪，老虎，羊头怪"
    ],
    "找出2个地府的三界群雄": [
        "地藏菩萨，白无常"
    ],
    "找出3个男性可选角色": [
        "龙太子，越星河，巨魔王"
    ],
    "找出常驻凌霄宝殿的3个角色": [
        "王母娘娘，嫦娥仙子，北斗星君"
    ],
    "找出2个与牛魔王有爱情纠葛的角色": [
        "铁扇公主，玉面狐狸"
    ],
    "找出2个封印型三界群雄": [
        "孙婆婆，飞霞"
    ],
    "找出3个女性可选角色": [
        "英女侠，喵千岁，骨精灵"
    ],
    "找出3个双叉岭的妖怪": [
        "熊山君，特处士，寅将军"
    ],
    "找出2个物攻三界群雄": [
        "孙悟空，大鹏王"
    ],
    "哪只召唤灵随身携带雨伞？": [
        "幽冥书生"
    ],
    "哪个妖怪曾今假扮天竺公主？": [
        "玉兔精"
    ],
    "哪个伙伴受到伤害时，攻击者有概率被封印？": [
        "嫦娥仙子"
    ],
    "哪个伙伴杀死单位后可以增加伤害？": [
        "大当家"
    ],
    "哪个召唤了拥有死亡召唤技能？": [
        "幽冥书生"
    ],
    "哪个召唤灵拥有力劈华山技能？": [
        "巨灵神将"
    ],
    "哪个神仙年幼时和父亲不合？": [
        "哪吒"
    ],
    "哪个神仙被称作托塔天王？": [
        "李靖"
    ],
    "哪些师父的弟子会封印类的师门技能？": [
        "菩提祖师",
        "月灵"
    ],
    "哪些伙伴会使用治疗法术？": [
        "唐僧，老鼠精"
    ],
    "哪个主角跟漠少君关系比较好？": [
        "虎头怪"
    ],
    "哪个伙伴会躲避每回合第一次攻击？": [
        "老鼠精"
    ],
    "哪个妖怪居住在毒敌山琵琶洞？": [
        "蝎子精"
    ],
    "哪个伙伴气血归零时，会触发寒冰护盾？": [
        "北海龙女"
    ],
    "哪个伙伴死亡后可以给队友加血？": [
        "惠岸行者"
    ],
    "哪些召唤灵必带水攻技能？": [
        "龟丞相，蚌仙子"
    ],
    "哪个神仙喜欢养狗？": [
        "二郎神"
    ],
    "龙宫的门派师父是谁？": [
        "龙海龙王"
    ],
    "月宫的门派师父是谁？": [
        "月灵"
    ],
    "狮搏技能最可能是谁创造的？": [
        "大大王"
    ],
    "女儿村的门派师傅是谁？": [
        "孙婆婆"
    ],
    "花果山的门派师父是？": [
        "超凡孙悟空"
    ],
    "下列谁是龙宫的三界群雄？": [
        "西海龙王"
    ],
    "跟月相有关的门派师父是谁？": [
        "月灵"
    ],
    "下列不是人族门派师傅的是？": [
        "长孙靖"
    ],
    "小雷音的门派师父是谁？": [
        "黄眉"
    ],
    "须弥海的门派师父是？": [
        "增长天王"
    ],
    "狮驼岭的门派师父是谁？": [
        "大大王"
    ],
    "化生寺的门派师父是谁？": [
        "空度禅师"
    ],
    "金箍棒是谁锻造的？": [
        "太上老君"
    ],
    "兑换高级藏宝图应该找谁？": [
        "偷偷怪"
    ],
    "下列哪些是二十八星宿？": [
        "奎木狼",
        "亢金龙",
        "柳土獐"
    ],
    "通晓过去与未来的无心是？": [
        "和尚"
    ],
    "谁将唐僧称为“御弟哥哥”？": [
        "女儿国王"
    ],
    "黑熊精被谁收做了守山大神？": [
        "观音菩萨"
    ],
    "避水金晶兽是谁的坐骑？": [
        "牛魔王"
    ],
    "速度最慢的治疗系伙伴是谁？": [
        "惠岸行者"
    ],
    "唐僧的徒弟中，谁法号悟能？": [
        "猪八戒"
    ],
    "魏征在梦中斩了谁？": [
        "泾河龙王"
    ],
    "“人参果”是谁种植的？": [
        "镇元子"
    ],
    "想要改变造型颜色应该找谁？": [
        "配色师"
    ],
    "谁想要和唐僧结婚？": [
        "女儿国王",
        "玉兔精",
        "蝎子精"
    ],
    "地涌夫人供奉了谁的牌位？": [
        "李靖",
        "哪吒"
    ],
    "西海三太子是谁？": [
        "小白龙"
    ],
    "谁在奈何桥边熬制孟婆汤？": [
        "孟婆"
    ],
    "谁是唐僧的杀父仇人？": [
        "刘洪",
        "李彪"
    ],
    "孙悟空找谁“借用”的如意金箍棒？": [
        "东海龙王"
    ],
    "唐僧是谁的义弟？": [
        "唐太宗"
    ],
    "寻找3个天命取经人": [
        "唐僧",
        "孙悟空",
        "猪八戒"
    ],
    "想购买召唤灵应该找谁？": [
        "花香香"
    ],
    "泾河龙王触犯天条后找谁请救？": [
        "唐太宗"
    ],
    "红孩儿的母亲是谁？": [
        "铁扇公主"
    ],
    "唐僧的父亲是谁？": [
        "陈光蕊"
    ],
    "宝图任务找谁领取？": [
        "店小二"
    ],
    "孙悟空请谁来帮忙战胜了九头虫？": [
        "二郎神"
    ],
    "是谁打翻了老君的炼丹炉造就了火焰山？": [
        "孙悟空"
    ],
    "谁因打破琉璃盏被贬出天界？": [
        "沙和尚"
    ],
    "木吒在观音菩萨座下称号为？": [
        "惠岸行者"
    ],
    "谁自称“平天大圣”？": [
        "牛魔王"
    ],
    "谁喜欢卷帘大将？": [
        "阿紫"
    ],
    "谁教会了孙悟空七十二变？": [
        "菩提祖师"
    ],
    "观音将佛祖的3个箍用给了谁？": [
        "孙悟空",
        "黑熊精",
        "红孩儿"
    ],
    "观音菩萨身边的善财童子是谁？": [
        "红孩儿"
    ],
    "泾河龙王打赌输给了谁？": [
        "袁守城"
    ],
    "“半路杀出个谁”表示措手不及？": [
        "程咬金"
    ],
    "西梁女国的国王是谁？": [
        "女儿国王"
    ],
    "使用降妖宝杖作为武器的是谁？": [
        "沙和尚"
    ],
    "象形技能最可能是谁创造的？": [
        "二大王"
    ],
    "60级可以携带以下哪些召唤灵出战？": [
        "鲛将军",
        "蚌仙子",
        "马面"
    ],
    "唐僧的母亲是谁？": [
        "殷温娇"
    ],
    "猪八戒最有可能吓到谁？": [
        "小朋友"
    ],
    "谁是金山寺住持？": [
        "法明长老"
    ],
    "谁受菩萨点化后化作白龙马？": [
        "小白龙"
    ],
    "说“地狱不空，誓不为佛”的是谁？": [
        "地藏王"
    ],
    "唐僧的徒弟中，谁法号悟净？": [
        "沙和尚"
    ],
    "想要寄存召唤灵应该找谁？": [
        "召唤灵仙子"
    ],
    "“敖广”是谁的名字？": [
        "东海龙王"
    ],
    "谁被封为了净坛使者？": [
        "猪八戒"
    ],
    "科举殿试是谁主持进行的？": [
        "李世民，玉皇大帝，阎罗王"
    ],
    "谁与北海龙子兄妹情深？": [
        "北海龙女"
    ],
    "鹰击技能最可能是谁创造的？": [
        "三大王"
    ],
    "消耗活力打工赚钱应该找谁？": [
        "颜如羽"
    ],
    "使用九齿钉耙作为武器的是谁？": [
        "猪八戒"
    ],
    "幽冥书生生前深爱的人是谁？": [
        "文秀"
    ],
    "运镖任务应该找谁？": [
        "郑镖头"
    ],
    "东海龙王的三子敖丙是谁打死的？": [
        "哪吒"
    ],
    "谛听是谁的坐骑？": [
        "地藏王"
    ],
    "想要结情缘该去找谁？": [
        "月老"
    ],
    "瞌睡了但没有家该去找谁？": [
        "酒店老板"
    ],
    "谁诏安孙悟空当了弼马温？": [
        "太白金星"
    ],
    "“孙悟空”的名字是谁起的？": [
        "菩提祖师"
    ],
    "是谁在围捕孙悟空时用金刚琢偷袭？": [
        "太上老君"
    ],
    "你获得的第一只召唤灵是什么？": [
        "野猪"
    ],
    "红孩儿对外公开的父亲是谁？": [
        "牛魔王"
    ],
    "谁自称“圣婴大王”？": [
        "红孩儿"
    ],
    "游戏中遇到不懂的问题该问谁？": [
        "梦幻精灵"
    ],
    "下列谁是龙宫的三界群雄": [
        "西海龙王"
    ],
    "谁又被称作“罗刹女”": [
        "铁扇公主"
    ],
    "谁更名为“程知节”？": [
        "程咬金"
    ],
    "姚太尉曾向谁求亲？": [
        "阿紫"
    ],
    "谁曾大闹天宫？": [
        "孙悟空"
    ],
    "谁成天找人帮他捉鬼？": [
        "钟馗"
    ]
}