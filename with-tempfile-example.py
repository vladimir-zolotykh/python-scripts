
import tempfile
import subprocess
import os
select_target_sh_func = """
#!/bin/bash
function select_target {
    target_list=(%s)
    PS3="Select Target: "
    select target in "${target_list[@]}"; do
 	    break
    done
    echo $target
}
select_target
"""

target_list = ["Target1", "Target2", "Target3"]

with tempfile.NamedTemporaryFile() as temp:
    temp.write(select_target_sh_func % ' '.join(map(lambda s : '\"%s\"' % str(s),target_list)))
    temp.flush()
    # bash: /var/folders/jm/4j4mq_w52bx2l5qwg4gt44580000gn/T/tmp00laDV: Permission denied
    subprocess.call(['chmod', '0777', temp.name])
    sh_proc = subprocess.Popen(["bash", "-c", temp.name], stdout=subprocess.PIPE)
    (output, err) = sh_proc.communicate()
    exit_code = sh_proc.wait()
    print output
