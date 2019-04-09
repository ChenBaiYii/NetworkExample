#!/usr/bin/python3
# xml rpc client


import xmlrpc.client


def main():
    proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:7001")
    print("here are the functions supported by this server:")
    for method_name in proxy.system.listMethods():  # 列出所有支持的 rpc 函数
        if method_name.startswith('system.'):
            continue

        signatures = proxy.system.methodSignature(method_name)
        if isinstance(signatures, list) and signatures:
            for signature in signatures:
                print("%s(%s)" % (method_name, signature))
        else:

            print("%s(...)" % (method_name,))

        method_help = proxy.system.methodHelp(method_name)  # 获取 rpc 函数的文档描述
        if method_help:
            print(' ', method_help)


if __name__ == '__main__':
    main()
