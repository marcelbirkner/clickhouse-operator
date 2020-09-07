import kubectl
import settings


def query(
        chi_name,
        sql,
        with_error=False,
        host="127.0.0.1",
        port="9000",
        user="default",
        pwd="",
        ns=settings.test_namespace,
        timeout=60,
):
    pod_names = kubectl.get_pod_names(chi_name, ns)
    pod_name = pod_names[0]
    for p in pod_names:
        if host in p:
            pod_name = p

    pwd_str = "" if pwd == "" else f"--password={pwd}"

    if with_error:
        return kubectl.launch(
            f"exec {pod_name}"
            f" -- "
            f"clickhouse-client -mn -h {host} --port={port} -u {user} {pwd_str} "
            f"--query=\"{sql}\""
            f" 2>&1",
            timeout=timeout,
            ns=ns,
            ok_to_fail=True,
        )
    else:
        return kubectl.launch(
            f"exec {pod_name}"
            f" -- "
            f"clickhouse-client -mn -h {host} --port={port} -u {user} {pwd_str} "
            f"--query=\"{sql}\"",
            timeout=timeout,
            ns=ns,
        )


def query_with_error(
        chi_name,
        sql,
        host="127.0.0.1",
        port="9000",
        user="default",
        pwd="",
        ns=settings.test_namespace,
        timeout=60,
):
    return query(chi_name, sql, True, host, port, user, pwd, ns, timeout)
