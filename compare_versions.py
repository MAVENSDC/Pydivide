def compare_versions():
    #import libraries
    import requests
    import os

    #access complete list of revision numbers on PyPI 
    pydivide_url = "https://pypi.python.org/pypi/pydivide/json"
    pd_pypi_vn = sorted(requests.get(pydivide_url).json()['releases'])
    
    #print PyPI version number
    print("PyPI PyDivide Version")
    pd_pypi_vn = pd_pypi_vn[-1]
    print(pd_pypi_vn)
    pd_pypi_vn = pd_pypi_vn.split(".")
    #convert to integer array for comparison
    pd_pypi_vn = [int(i) for i in pd_pypi_vn]
    
    #find current directory out of which code is executing
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print("Your PyDivide Version in " + dir_path)
    version_path = dir_path + '/version.txt'
    #open version.txt in current directory and read
    with open(version_path) as f:
        cur_vn = f.readlines()
    cur_vn = "".join(cur_vn)
    print(cur_vn)
    cur_vn = cur_vn.split(".")
    #convert to integer array for comparison
    cur_vn = [int(i) for i in cur_vn]

    #for each item in version number array [X.Y.Z]
    for i in range(len(cur_vn)):
        #if current item > PyPI item (hypothetical), break, latest version is running
        if cur_vn[i] > pd_pypi_vn[i]:
            old_flag = 0
            break
        #if current item = PyPI item, continue to check next item
        elif cur_vn[i] == pd_pypi_vn[i]:
            old_flag = 0
            continue
        #if current item < PyPI item, indicative of old version, throw flag to initiate warning
        else:
            old_flag = 1
            break

    #if not running latest version, throw warning
    if old_flag == 1:
        print("")
        print('****************************** WARNING! ******************************')
        print('*                                                                    *')
        print('*          You are running an outdated version of PyDivide.          *')
        print('*            Sync your repository for the latest updates.            *')
        print('*                                                                    *')
        print('****************************** WARNING! ******************************')
    #else inform user of updated status
    else:
        print("")
        print('You are running the latest version of PyDivide.')
compare_versions()