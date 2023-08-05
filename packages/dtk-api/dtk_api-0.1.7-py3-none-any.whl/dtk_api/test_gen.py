import os
import sys

from .gen import *
from .test_shared import get_id, get_dtk_sync, get_goods_id


def convert_name_to_py_class_name(name: str) -> str:
    parts = name.split("_")
    out = "".join(map(lambda x: x.capitalize(), parts))
    return f"{out}Resp"


def gen_with_class_name(class_name: str, data: dict) -> str:
    fields = []
    sub_codes = []
    for name, value in data.items():
        typ = type(value)
        if typ is str:
            fields.append(f"""    {name}: str = Field(...)""")
        elif typ is int:
            fields.append(f"""    {name}: int = Field(...)""")
        elif typ is float:
            fields.append(f"""    {name}: float = Field(...)""")
        elif typ is dict:
            sub_name, sub_code = gen_sub_field(class_name, name, value)
            fields.append(f"""    {name}: {sub_name} = Field(...)""")
            sub_codes.append(sub_code)
        elif typ is list:
            if len(value) >= 1:
                if type(value[0]) == dict:
                    sub_name, sub_code = gen_sub_field(class_name, name, value[0])
                    fields.append(f"""    {name}: List[{sub_name}] = Field(...)""")
                    sub_codes.append(sub_code)
                elif type(value[0]) == str:
                    fields.append(f"""    {name}: List[str] = Field(...)""")
                else:
                    print(f"{type(value[0])} is not handled")
                    sys.exit(3)
            else:
                fields.append(f"""    {name}: list = Field(...)""")
        else:
            print(f"未知的类型: {typ=}")
            sys.exit(1)
    field_code = "\n".join(fields)
    sub_field_code = "\n".join(sub_codes)

    return f"""
{sub_field_code}
class {class_name}(BaseModel):
{field_code}
"""


# return value:
# 1st is sub class name
# 2nd is code
def gen_sub_field(class_name: str, field_name: str, data: dict) -> (str, str):
    sub_name = f"{class_name}{field_name.capitalize()}"

    class_dt = gen_with_class_name(sub_name, data)

    return sub_name, class_dt


def gen_one_data(name: str, data: dict) -> str:
    class_name = convert_name_to_py_class_name(name)

    fields = []
    sub_codes = []
    for name, value in data.items():
        typ = type(value)
        if typ is str:
            fields.append(f"""    {name}: str = Field(...)""")
        elif typ is int:
            fields.append(f"""    {name}: int = Field(...)""")
        elif typ is float:
            fields.append(f"""    {name}: float = Field(...)""")
        elif typ is dict:
            sub_name, sub_code = gen_sub_field(class_name, name, value)
            fields.append(f"""    {name}: {sub_name} = Field(...)""")
            sub_codes.append(sub_code)
        elif typ is list:
            if len(value) >= 1:
                if type(value[0]) == dict:
                    sub_name, sub_code = gen_sub_field(class_name, name, value[0])
                    fields.append(f"""    {name}: List[{sub_name}] = Field(...)""")
                    sub_codes.append(sub_code)
                elif type(value[0]) == str:
                    fields.append(f"""    {name}: List[str] = Field(...)""")
                else:
                    print(f"{type(value[0])} is not handled")
                    sys.exit(3)
            else:
                fields.append(f"""    {name}: list = Field(...)""")
        else:
            sys.exit(1)

    field_code = "\n".join(fields)
    sub_field_code = "\n".join(sub_codes)

    return f"""
{sub_field_code}
class {class_name}(BaseModel):
{field_code}
"""


def write_to_file(code: str):
    out_file = os.path.join(os.path.dirname(__file__), "dt_resp_v2.py")
    with open(out_file, "a") as fp:
        fp.write(code)


def test_gen_category_get_super_category():
    dtk = get_dtk_sync()
    ret = dtk.category_get_super_category()
    assert ret["code"] == 0
    o = gen_one_data("category_get_super_category", ret["data"][0])
    write_to_file(o)


def test_goods_price_trend():
    dtk = get_dtk_sync()
    args = GoodsPriceTrendArgs(id=get_id())
    ret = dtk.goods_price_trend(args)
    assert ret["code"] == 0
    o = gen_one_data("goods_price_trend", ret["data"][0])
    write_to_file(o)


def test_goods_dtk_search():
    dtk = get_dtk_sync()
    args = GoodsGetDtkSearchGoodsArgs(keyWords="手机", pageId=1, pageSize=10)
    ret = dtk.goods_get_dtk_search_goods(args)
    assert ret["code"] == 0
    o = gen_one_data("goods_get_dtk_search_goods", ret["data"])
    write_to_file(o)


def test_tb_service_get_privilege_link():
    dtk = get_dtk_sync()
    args = TbServiceGetPrivilegeLinkArgs(goodsId=get_goods_id())
    ret = dtk.tb_service_get_privilege_link(args)
    assert ret["code"] == 0
    o = gen_one_data("tb_service_get_privilege_link", ret["data"])
    write_to_file(o)


def test_goods_get_ranking_list():
    dtk = get_dtk_sync()
    args = GoodsGetRankingListArgs(rankType=1)
    ret = dtk.goods_get_ranking_list(args)
    assert ret["code"] == 0
    o = gen_one_data("goods_get_ranking_list", ret["data"][0])
    write_to_file(o)


def test_goods_get_goods_details():
    dtk = get_dtk_sync()
    args = GoodsGetGoodsDetailsArgs(id=get_id())
    ret = dtk.goods_get_goods_details(args)
    assert ret["code"] == 0
    o = gen_one_data("goods_get_goods_details", ret["data"])
    write_to_file(o)


def test_tb_service_get_brand_list():
    dtk = get_dtk_sync()
    args = TbServiceGetBrandListArgs(pageId=1, pageSize=10)
    ret = dtk.tb_service_get_brand_list(args)
    assert ret["code"] == 0
    o = gen_one_data("tb_service_get_brand_list", ret["data"][0])
    write_to_file(o)


def test_goods_nine_op_goods_list():
    dtk = get_dtk_sync()
    args = GoodsNineOpGoodsListArgs(pageId=1, pageSize=10, nineCid=1)
    ret = dtk.goods_nine_op_goods_list(args)
    assert ret["code"] == 0
    o = gen_one_data("goods_nine_op_goods_list", ret["data"])
    write_to_file(o)


def test_tb_service_get_tb_service():
    dtk = get_dtk_sync()
    args = TbServiceGetTbServiceArgs(pageNo=1, pageSize=10, keyWords="苹果")
    ret = dtk.tb_service_get_tb_service(args)
    assert ret["code"] == 0
    o = gen_one_data("tb_service_get_tb_service", ret["data"][0])
    write_to_file(o)


def test_category_get_top100():
    dtk = get_dtk_sync()
    ret = dtk.category_get_top100()
    print(ret["data"])
    assert ret["code"] == 0
    o = gen_one_data("category_get_top100", ret["data"])
    write_to_file(o)


def test_goods_get_goods_list():
    dtk = get_dtk_sync()
    args = GoodsGetGoodsListArgs()
    ret = dtk.goods_get_goods_list(args)
    assert ret["code"] == 0
    o = gen_one_data("goods_get_goods_list", ret["data"][0])
    write_to_file(o)


def test_slot_code():
    slot = f"""
CategoryDdqGoodsListResp = Any
CategoryGetTbTopicListResp = Any
GoodsActivityCatalogueResp = Any
GoodsActivityGoodsListResp = Any
GoodsExclusiveGoodsListResp = Any
GoodsExplosiveGoodsListResp = Any
GoodsFirstOrderGiftMoneyResp = Any
GoodsFriendsCircleListResp = Any
GoodsGetCollectionListResp = Any
GoodsGetGoodsListResp = Any
GoodsGetNewestGoodsResp = Any
GoodsGetOwnerGoodsResp = Any
GoodsGetStaleGoodsByTimeResp = Any
GoodsTopicCatalogueResp = Any
GoodsListSimilerGoodsByOpenResp = Any
GoodsListSuperGoodsResp = Any
GoodsLivematerialGoodsListResp = Any
GoodsPullGoodsByTimeResp = Any
GoodsSearchSuggestionResp = Any
GoodsTopicCatalogue = Any
GoodsTopicGoodsListResp = Any
TbServiceActivityLinkResp = Any
TbServiceCreatTaokoulingResp = Any
TbServiceGetOrderDetailsResp = Any
TbServiceParseContentResp = Any
TbServiceParseTaokoulingResp = Any
TbServiceTwdToTwdResp = Any
"""
    write_to_file(slot)
