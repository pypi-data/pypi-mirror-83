from subprocess import Popen, STDOUT, PIPE

from .data.shell_ouputs import *

CMD = "/tmp/.tox/python/bin/tcv"


def test_help_exit_code():
    call = Popen(["sh", CMD, "-h"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == help_out
    assert code == 1

    call = Popen(["sh", CMD, "--help"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == help_out
    assert code == 1


def test_invalid_option():
    call = Popen(["sh", CMD, "-hx"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == wrong_option_out
    assert code == 1

    call = Popen(["sh", CMD, "--help_wrong"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == wrong_option_out
    assert code == 1


def test_version_exit_code():
    call = Popen(["sh", CMD, "-V"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert code == 1

    call = Popen(["sh", CMD, "--version"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert code == 1


def test_no_args_fail():
    call = Popen(["sh", CMD], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == no_config_out
    assert code == 1


def test_only_config_fail():
    call = Popen(["sh", CMD, "-c=/tmp/config.yml"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == no_function_out
    assert code == 1

    call = Popen(["sh", CMD, "--config=/tmp/config.yml"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == no_function_out
    assert code == 1


def test_only_function_fail():
    call = Popen(["sh", CMD, "-fn=preprocess"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == no_config_out
    assert code == 1

    call = Popen(["sh", CMD, "--function=preprocess"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == no_config_out
    assert code == 1


def test_wrong_function():
    call = Popen(["sh", CMD, "-c=dummy -fn=preprocess_wrong"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == wrong_function_out
    assert code == 1

    call = Popen(["sh", CMD, "-c=dummy --function=preprocess_wrong"], stderr=STDOUT, stdout=PIPE)
    out, code = call.communicate()[0], call.returncode
    assert out == wrong_function_out
    assert code == 1
