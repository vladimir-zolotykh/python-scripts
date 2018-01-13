import os

import subprocess
import sys
import re

from optparse import OptionParser

def pselect(choices):
    """Ask a user to select one of the enumerated choices. Return the selection."""
    dict2 = dict((i, f) for i, f in enumerate(f for f in choices))
    row=["{: >3} {:<}".format(k,v) for k,v in sorted(dict2.items())]
    choice = None
    while choice is None:
        for a, b, c in zip(row[::3], row[1::3], row[2::3]):
            print '{:<30}{:<30}{:<}'.format(a, b, c)
        choice = dict2.get(int(raw_input("Selection? ")))
        if not choice:
            print 'Please make a valid selection'
        else:
            print 'You selected {:s}'.format(choice)

    return (choice)

class Cov0(object):
    COV_INTDIR=""
    COV_HTMLDIR=""
    BLD_TARGET=""
    BLD_VARIANT=""
    BUILD_CMD="$BUNNY_BIN/BunnyBuild $BLD_TARGET $BLD_VARIANT"
    COV_CA_COND=""
    BUNNY_BIN=""
    COV_BIN=""
    def exec_cmd (self, cmd):
        ret = subprocess.call(cmd, shell=True)
        return (ret)
    def clean0(self, rm_cmd):
        ret = subprocess.call(rm_cmd, shell=True)
        return ret
    
class Cov(Cov0) :
    def __init__(self, cwd):
        self.cwd = cwd
        self.COV_BIN = "/opt/cov-analysis-linux-8.5.0/bin"  # VBox
        if os.path.isdir("/opt/cov-analysis-linux64-8.5.0/bin"):
            self.COV_BIN ="/opt/cov-analysis-linux64-8.5.0/bin"
        self.COV_HTMLDIR=os.path.join(cwd,"/coverity/report")

        # On VBox /home partition is too small and we have to use the larger / partion
        # /coverity/report has to be created manually beforehand , and given ownership visteon:visteon

        if os.path.isdir("/coverity/report"):
            self.COV_HTMLDIR="/coverity/report"
        self.COV_INTDIR=os.path.join(cwd, "/coverity/intdir")
        self.COV_HTMLDIR=os.path.join(cwd, "/coverity/report")
        self.BUNNY_BIN=os.path.join(cwd, "/Tools/Bunny/Bunny/bin")
        #COV_CA_CONF=$COV_BIN/visteon_Ruleset_v4_0.json
        self.COV_CA_CONF=os.path.join(self.COV_BIN, "/visteon_Ruleset_v4_0.json")
    def get_release(self, url):
        if super(Cov).exec_cmd('curl -0 {:s}'.format(url)) == 0:
            release7z = os.path.basename(url)
            release_dir = re.search('\.(Release-.*)_Sources\.7z$', release7z)
            if release_dir:
                release_dir = release_dir.group(1)
                if super(Cov).exec_cmd("7z -o{:s} {:s}".format(release_dir, release7z)) == 0:
                    os.chdir(release_dir)
                    super(Cov).exec_cmd("ln -s ~/Documents/Stash/pmt/MFA2/Coverity/pcov.py .")
                else:
                    print("7z command failed")
            else:
                print('Wrong release name {:s} supplied.'.format(release7z))
        else:
            print('Curl command failed.')
    def get_target(self):
        target_list=["UICockpit.WIMService", "UICockpit.UIServerProcess", "DI.VipProxyProcess",
                     "HMI.ClusterEntry", "HMI.ClusterHigh", "DI.IPCServer",
                     "HMI.HMI_ASILOverlayProcess", "HMI.HUD", "DI.DIOnOffProcess"]
        self.BLD_TARGET=pselect(target_list)
    def get_variant(self):
        delispace_dir=os.path.join(self.cwd, "/DeliSpace")
        if not os.path.isdir(delispace_dir):
            print('{:s}: doesn'' exist')
        variant_list = [d for d in os.listdir(delispace_dir) if os.path.isdir(d)]
        self.BLD_VARIANT=pselect(variant_list)
    def clean_space(self):
        super(Cov).clean0('rm -rf ProductSpace/* InterSpace/*')
    def clean_intdir(self):
        super(Cov).clean0('rm -rf {:s}/*'.format(self.COV_INTDIR))
    def clean_htmldir(self):
        super(Cov).clean0('rm -rf {:s}/*'.format(self.COV_HTMLDIR))
    def clean(self):
        self.clean_space()
        self.clean_intdir()
        self.clean_htmldir()

    def build(self):
        self.BUILD_CMD = '{:s}/BunnyBuild {:s} {:s}'\
            .format(self.BUNNY_BIN, self.BLD_TARGET, self.BLD_VARIANT)
        cmd = '{:s}/cov-build --dir {:s} --preprocess-first {:s}'.format(self.COV_BIN, self.COV_INTDIR, self.BUILD_CMD)
        super(Cov,self).exec_cmd(cmd)

    def analyze(self):
        cmd='{:s}/cov-analyze --dir {:s} --disable-default --enable-parse-warnings --enable-callgraph-metrics'
        '--enable-fnptr --enable-virtual --inherit-taint-from-unions --analysis-settings {:s}'\
            .format(self.COV_BIN, self.COV_INTDIR, self.COV_CA_CONF)
        super(Cov,self).exec_cmd(cmd)

    def format_errors(self):
        cmd='{:s}/cov-format-errors --dir {:s} --html-output {:s} --noX --exclude-files ".*/.h'\
            .format(self.COV_BIN, self.COV_INTDIR, self.COV_HTMLDIR)
        super(Cov, self).exec_cmd(cmd)

if __name__ == "__main__" :
    cwd = os.getcwd()

    Cov2 = Cov(cwd)
    usage = """
    Usage: %prog -g <RELEASE_URI>
                 -z
                 -[bB]
                 -f
    """
    parser = OptionParser(usage=usage)
    parser.add_option("-g", dest="release_url", action="store",
                      help="Release (sources.zip) url")
    parser.add_option("-z", action="store_true", dest="clean_build",
                      help="Clean all intermediate files")
    parser.add_option("-b", dest="build_only",
                      help="Do Coverity build only")
    parser.add_option("-B", dest="build_only", action="store_false",
                      help="Do full Coverity run (build, analyze, format errors)")
    parser.add_option("-a", dest="analyze_only", action="store_true",
                      help="Do Coverity analyze only")
    parser.add_option("-f", dest="format_only", action="store_true",
                      help="Format errors only")

    options, args = parser.parse_args()

    if options.release_url :
        Cov2.get_release(options.release_url)
    if options.clean_build and not options.release_url:
        Cov2.clean()
    if options.build_only:
        Cov2.build()
    else:
        Cov2.build()
        Cov2.analyze()
        Cov2.format_errors()
        sys.exit(0)

    if options.anlyze_only:
        Cov2.analyze()
    if options.format_only:
        Cov2.format_errors()


