from core.experiment import Experiment, ExperimentParameter
import logging
import os


class XquicParameter(ExperimentParameter):
    XQUICSERVER = "xquicServer"
    XQUICCLIENT = "xquicClient"

    def __init__(self, experiment_parameter_filename):
        super(XquicParameter, self).__init__(experiment_parameter_filename)
        self.default_parameters.update({
            XquicParameter.XQUICSERVER : "xquicServer",
            XquicParameter.XQUICCLIENT : "xquicClient",
        })


class XquicScenario(Experiment):
    NAME = "xquic"
    PARAMETER_CLASS = XquicParameter

    def __init__(self, experiment_parameter_filename, topo, topo_config):
        super(XquicScenario, self).__init__(experiment_parameter_filename, topo, topo_config)
        self.load_parameters()
        # self.ping()

    def load_parameters(self):
        super(XquicScenario, self).load_parameters()
        self.server = self.experiment_parameter.get(XquicParameter.XQUICSERVER)
        self.client = self.experiment_parameter.get(XquicParameter.XQUICCLIENT)

    # def prepare(self):
    #     super(XquicScenario, self).prepare()

    def xquic_command(
            self,
            type,
            server_ip='127.0.0.1',
            server_port=8443,
            file_size=304857600,
            # redis_server='10.0.0.123',
            # redis_port=6379,
            # rlcc_flag=4321,
        ):
            """
                type : 'client' 'server'
                50Mb/?B : 52428800
                10M : 10485760
            """
            if type == 'server':
                return f"{self.server} -l e > /dev/null"
            elif type == 'client':
                cmd = f"{self.client} -l e -a {server_ip}" \
                    + f" -p {server_port} -s {file_size} -c b -T"  # -c b : default cc bbr
                return cmd


    def get_client_cmd(self, server_ip):
        s = self.xquic_command(type="client", server_ip=server_ip)
        logging.info(s)
        return s

    def get_server_cmd(self):
        s = self.xquic_command(type="server")
        logging.info(s)
        return s

    def clean(self):
        super(XquicScenario, self).clean()

    def run(self):
        cmd = self.get_server_cmd()
        cmd += " &"  # run backend
        self.topo.command_to(self.topo_config.server, cmd)

        self.topo.command_to(self.topo_config.client, "sleep 2")
        cmd = self.get_client_cmd(server_ip=self.topo_config.get_server_ip())
        self.topo.command_to(self.topo_config.client, cmd)
        self.topo.command_to(self.topo_config.client, "sleep 2")