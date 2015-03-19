from backend.user.json import JsonUserBackend
from core.dsa import Dsa
from core.instance import Instance
from multiprocessing import Process

if __name__ == '__main__':
    instances = []

    user_backend = JsonUserBackend('users.json')
    try:
        user_backend.add_user('giovanni', 'admin')
        user_backend.add_user('beatrice', 'user')
        user_backend.store()
    except Exception:
        pass



    dsa1 = Instance(Dsa('DSA1', 'localhost', 389, user_backend=user_backend))
    dsa2 = Instance(Dsa('DSA2', 'localhost', 636, cert_file='cert-serv.pem', key_file='key-serv.pem', user_backend=user_backend))

    instances.append(dsa1)
    instances.append(dsa2)

    for instance in instances:
        instance.process = Process(target=instance.dsa.start)
        instance.process.start()

    print('started %d instances' % (len(instances)))

    for instance in instances:
        instance.process.join()

    print('sldap3 done')
