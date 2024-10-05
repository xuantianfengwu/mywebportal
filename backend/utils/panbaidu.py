
import requests

def get_pan_file_names(dir, cookie):
    """
        根据百度网盘网页版上的Cookie，和链接里的dir参数，获取dir下边的全部文件名
    """
    url = 'https://pan.baidu.com/api/list?clienttype=0&app_id=250528&web=1&dp-logid=83154400288756880067&order=time&desc=1&dir={}&page=1'.format(dir)

    headers = {
        'Cookie': cookie,
        'Host': 'pan.baidu.com'
    }

    resp = requests.get(url, headers=headers)
    resp_json = resp.json()

    f_lst = resp_json['list']
    f_lst = sorted(f_lst, key=lambda f: f['server_filename'])

    f_id_lst = [f['fs_id'] for f in f_lst]
    f_name_lst = [f['server_filename'] for f in f_lst]

    for f_id, f_name in zip(f_id_lst,f_name_lst):
        print(f_name)

# Request URL: https://pan.baidu.com/api/filemanager?async=2&onnest=fail&opera=rename&bdstoken=d1c765f578d8d1b224821de32bfdcb6f&clienttype=0&app_id=250528&web=1&dp-logid=83154400288756880091
# filelist =
# [{"id":139651412157306,
#   "path":"/1. 资料 & 教程/量化投资/量化投资研报资料/01 国泰君安/1.3 国泰君安_股指期货系列/国泰君安-20080630-股指期货系列报告之十七：股指期货对现货走势的引导与预测：理论、实证与案例.pdf",
#   "newname":"20080630-国泰君安-股指期货系列报告之十七：股指期货对现货走势的引导与预测：理论、实证与案例.pdf"}
# ]

if __name__ =='__main__':
    dir = '%2F1.%20资料%20%26%20教程%2F量化投资%2F量化投资研报资料%2F12%20东方证券%2F12.3%20东方证券-因子选股系列'
    cookie = 'BIDUPSID=428C6DCF3A848A2FC0B1C3EFCACB2E63; PSTM=1654616258; BDUSS=GRZc3JzbjFrTnYxcGVHQ0g2aFBCRUlWZXR-NVJYfkZzWTBLaVQzcTZPTzJkYzVpRVFBQUFBJCQAAAAAAAAAAAEAAAAaoSINeHVhbnRpYW5mZW5nd3UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALbopmK26KZic; BDUSS_BFESS=GRZc3JzbjFrTnYxcGVHQ0g2aFBCRUlWZXR-NVJYfkZzWTBLaVQzcTZPTzJkYzVpRVFBQUFBJCQAAAAAAAAAAAEAAAAaoSINeHVhbnRpYW5mZW5nd3UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALbopmK26KZic; BAIDUID=428C6DCF3A848A2FC0B1C3EFCACB2E63:SL=0:NR=10:FG=1; Hm_lvt_95fc87a381fad8fcb37d76ac51fefcea=1665207942; PANWEB=1; csrfToken=8opz7flJJqwvH2AQZGkno9gc; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1665021543,1667074902; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1667074943; MCITY=-289%3A; BDSFRCVID=m6kOJeC624VHSeOjrIUChd9-JZShd4RTH6ao2LvYL-X_Z2viNxxAEG0PaM8g0KA-hILjogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF=tRk8oK-atDvDqTrP-trf5DCShUFsQq0jB2Q-XPoO3KtB8f3hMl6RhPuA5hb-L6jiW5cpoMbgylRp8P3y0bb2DUA1y4vpKbvyLeTxoUJ2XhrPDfcoqtnWhfkebPRiWTj9QgbLVpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wDT8hD6P_-pO0-tcJM4o3LRj55RTjDb7GbKTjhPrMMUrCWMT-MTryKKtXBx3Gjxc5hPcl5bt83H5iBb5ptanRhlRNLfTIht5xj-5C-UKZbp7yQfQxtNRJMhrIaxcvKJ79hf7obUPUXa59LUvLfgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLJK-WMKI6j5Rb5nbHMlo3KC62aJ3L_JvvWJ5TMC_m3x76bf4qK4rP3-vbf4jZhfOS5IbCShPC-tPKXbK4X2cvyhIHbD5wXPnp3l02VbjEe-t2yUoDM-rratRMW23roq7mWn6rsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjj6jK4JKDG_OJjJP; BAIDUID_BFESS=428C6DCF3A848A2FC0B1C3EFCACB2E63:SL=0:NR=10:FG=1; BDSFRCVID_BFESS=m6kOJeC624VHSeOjrIUChd9-JZShd4RTH6ao2LvYL-X_Z2viNxxAEG0PaM8g0KA-hILjogKKL2OTHm_F_2uxOjjg8UtVJeC6EG0Ptf8g0f5; H_BDCLCKID_SF_BFESS=tRk8oK-atDvDqTrP-trf5DCShUFsQq0jB2Q-XPoO3KtB8f3hMl6RhPuA5hb-L6jiW5cpoMbgylRp8P3y0bb2DUA1y4vpKbvyLeTxoUJ2XhrPDfcoqtnWhfkebPRiWTj9QgbLVpQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0MBCK0hD0wDT8hD6P_-pO0-tcJM4o3LRj55RTjDb7GbKTjhPrMMUrCWMT-MTryKKtXBx3Gjxc5hPcl5bt83H5iBb5ptanRhlRNLfTIht5xj-5C-UKZbp7yQfQxtNRJMhrIaxcvKJ79hf7obUPUXa59LUvLfgcdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLJK-WMKI6j5Rb5nbHMlo3KC62aJ3L_JvvWJ5TMC_m3x76bf4qK4rP3-vbf4jZhfOS5IbCShPC-tPKXbK4X2cvyhIHbD5wXPnp3l02VbjEe-t2yUoDM-rratRMW23roq7mWn6rsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjj6jK4JKDG_OJjJP; delPer=0; PSINO=5; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; ZD_ENTRY=google; __bid_n=18562477347e16f5bd4207; FEID=v10-6f6ebede9a6ae08a9951436b4c1328b44e702e3e; __xaf_fpstarttimer__=1672391127913; __xaf_thstime__=1672391127960; __xaf_fptokentimer__=1672391127970; ZFY=CRK:AYE89oDA6PwXXUPzDULSRrzGRPqQE2HBMCWA6I0c:C; H_PS_PSSID=36554_37647_37551_38018_36920_37989_36803_37935_37900_26350_37881; STOKEN=c9a3b276db8a94a75d9834234b54853c4538553d5f1478812293da0cbf12d491; newlogin=1; ndut_fmt=207F09B1ED9DCE5D0462B9C0453C8A454EA7B6F495349D3D0031CE48098EC317; ab_sr=1.0.1_MTVhOWI4MDFmMzFmOWZiMWQ4YmViMDQ3YzI0OGIzYmZlOTA3M2M0ZjA0YzVjNTRlN2MwZjAzNDExOTg1NDRlYTEyNzJmNWY2MGE2YmJjNTQzNzZhOTBkOTU2YmNjYjJiNDk1NTkwZmMwYjc1YmNjZWNiZjUzOWViMzIxNmM1YzQ3YWJkZmFmOGIxMWEzMDI5NTVmNGVkOGZlMWYwYzMwZGY2OWEyMGQwNWNiNmNkYzEzMzMyZTZjOTAwNDE3Y2Mx; FPTOKEN=RpinFoGGEMOaxeBJJ55vDR4P4P6wZ9hdzPo3K4tU9VjF+WcSYFAkcXNwufyTV8wuN9G9fHgzoDDTIrnIaOuqx1A+0Topw3db4ZuAeDa8wfJwdHRCona3KwPQrPaM2G56gl7zGntje61GVSjwTXj4KopmuTlEP/cTKtgLKmThGbgCX7fSjEGrF24k79gFkndDPBQgFDBzwhSFbQu/uEdmdsWpt0trrU7lqiMf0KAkX1Crq9SgFYW7BqsLPRYANFC2RFu6G2LpMmwByd0y1n8n2EKhqudQMXLtR7ZaVHV9HSyhAMtuTYxWO7SqoUbia2LRziargm2+BNGb9XymgO5MHPi/Q1b4HwSXSgryZwFljnAmDZIdhXGbCZknAKeTZ7mtjPwCWKv98xJlILI77iJWoA==|H853eJW7qNekrXe1aXk0ErbUtNWVyCEUy6H50/wfO10=|10|d8ac0791a641b67ec2f8c9fec970d15b; BA_HECTOR=ah0ga10h2l058ka0al8k81ke1hs4ss21l; PANPSC=10385808530515163716%3AinYEMI9z4kryyG24r6pUMlcS2d9ns3O5V6FSZpa0R%2F3ssJv710BXryrPpcleMcayK9sKmG0jScymZy4GMW9U1yMhbb%2F7vRDwjZoYkL69Ous2jyb7JodIivKBB5%2BWSCTpbaC532AuNi3w0iRW66wpcZHaF0pmZEfIFyjhYr32wvKMhdDZUgg4IhXn03omd1eVPIwegva2ZpDyCymUoOM3enQB4yIxzI1YbwtT47bEE%2Fk%3D; AB_EXPERIMENT=%7B%22PC_SESSION_COOKIE_SWITCH%22%3A%22ON%22%2C%22group_cloud_smallflow%22%3A%22%22%2C%22ORDER_SIX_MONTH_CHECK%22%3A%22ON%22%2C%22group_smallflow%22%3A%22off%22%2C%22CHROME80_SET_COOKIE%22%3A%22ON%22%2C%22group_smallflow_uri%22%3A%22%22%2C%22rccGetChannelInfoSink%22%3A%22ON%22%7D'
    get_pan_file_names(dir, cookie)
