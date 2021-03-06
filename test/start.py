from multiprocessing import Process

from sldap3 import JsonUserBackend, Dsa, Instance


if __name__ == '__main__':
    instances = []

    user_backend = JsonUserBackend('localhost-users.json')
    user_backend.add_user('giovanni', 'admin', 'password')
    user_backend.add_user('beatrice', 'user', 'password')
    user_backend.store()

    dsa1 = Instance(Dsa('DSA1', 'localhost', cert_file='server-cert.pem', key_file='server-key.pem', user_backend=user_backend))
    dsa2 = Instance(Dsa('DSA2', 'localhost', port=1389, user_backend=user_backend))

    instances.append(dsa1)
    instances.append(dsa2)

    if len(instances) > 1:
        for instance in instances:
            instance.process = Process(target=instance.dsa.start)
            instance.process.start()

        print('started %d instances' % (len(instances)))

        for instance in instances:
            instance.process.join()
    elif len(instances) == 1:
        instances[0].dsa.start()

    print('sldap3 done')
