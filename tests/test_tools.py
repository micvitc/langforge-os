from langforge_os.tools import check_sys_tool, run_process, run_python


def test_check_sys_tool():
    result = check_sys_tool.invoke("check")
    assert "CPU Info" in result
    assert "Memory Info" in result
    assert "Disk Info" in result


def test_run_process():
    result = run_process.invoke("ls")
    assert result


def test_run_python():
    result = run_python.invoke('print("Hello, World!")')
    assert result == "Hello, World!\n"
