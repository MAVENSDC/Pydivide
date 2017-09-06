def compare_versions():
    import requests
    #import subprocess
    
    pytplot_url = "https://pypi.python.org/pypi/pytplot/json"
    pydivide_url = "https://pypi.python.org/pypi/pydivide/json"
    
    pt_git_vn = sorted(requests.get(pytplot_url).json()['releases'])
    pd_git_vn = sorted(requests.get(pydivide_url).json()['releases'])
    
    print("PyPI PyTplot Version")
    print(pt_git_vn[-1])
    print("")
    print("PyPI PyDivide Version")
    print(pd_git_vn[-1])
    
    

compare_versions()