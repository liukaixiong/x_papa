login_user = {
    # 帐号 : 密码
    # "18321006757": "lkx19940820",
    "17621253557": "lkx19940820"
}

default_cookie = "SCF=AgsMYeUS_Xn7Sv-RHCdXu5PZ5apgbcckmSH4TXTC0j0_sdxJaQMS8O5uhNsjzLkwESXCmV_WS6u9qKXresycyH4.; SUB=_2A25woqnCDeRhGeBP41oQ8CrPyDiIHXVQbDeKrDV6PUJbkdAKLW_ikW1NRQuJxF9Rizwbvt9A1XNpX3bcKRrXaYBX; SUHB=0IIVGa3ocnD06o; SSOLoginState=1571215762; MLOGIN=1; _T_WM=57051285649; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803"

login_cookies = [
    {
        "username": "18321006757",
        "cookie": default_cookie
    },
    {
        "username": "17621253557",
        "cookie": "ALF=1573807961; SCF=Amp0K_iWqOQXNBAacw3C0u_dVbzxhJVtBjTuuLjNPTIUwjCSpsN4zYkvdf17DN9zbo_fh5WfSknvT3eQrWiWyLE.; SUB=_2A25woqoJDeRhGeFN6lsQ8CjEzz6IHXVQbDZBrDV6PUJbktAKLWXkkW1NQE90C3td9m_AD0lSX0bd-VprdrnDJJ3-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh4AB5YrNMTkU_5BT6Bd0d_5JpX5KzhUgL.FoM0eK.pehqRShz2dJLoIX5LxK-LBKqL1hzLxKqLBozL1K5LxKqL1KnLBK-LxK.LBKeL12Hki--fi-2ciKnEi--ci-zEiK.7i--4iKLFi-2R; SUHB=03oFUfAOqoFuo5; SSOLoginState=1571215962; MLOGIN=1; _T_WM=61913112788; WEIBOCN_FROM=1110006030; M_WEIBOCN_PARAMS=uicode%3D10000011%26fid%3D102803"
    }]


def gen_cookies():
    for cookie in login_cookies:
        yield cookie
