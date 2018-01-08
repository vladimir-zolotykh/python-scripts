import subprocess

class Cov0:
    COV_INTDIR=""
    COV_HTMLDIR=""
    BUILD_CMD=""
    COV_CA_COND=""
    COV_BIN='/opt/cov-analysis-linux-8.5.0/bin'
    def exec_cmd (self, cmd):
        ret = subprocess.call(cmd, shell=True)
        return (ret)
    def clean0(self, rm_cmd):
        ret = subprocess.call(rm_cmd, shell=True)
        return ret
    
class Cov(Cov0) :
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