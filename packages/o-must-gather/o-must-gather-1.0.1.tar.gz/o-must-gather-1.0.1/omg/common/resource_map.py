from omg.cmd.get.from_yaml import from_yaml
from omg.cmd.get.get_project import get_project

from omg.cmd.get.simple_out import simple_out
from omg.cmd.get.node_out import node_out
from omg.cmd.get.pod_out import pod_out
from omg.cmd.get.project_out import project_out
from omg.cmd.get.co_out import co_out
from omg.cmd.get.csr_out import csr_out
from omg.cmd.get.cv_out import cv_out
from omg.cmd.get.mcp_out import mcp_out
from omg.cmd.get.mc_out import mc_out
from omg.cmd.get.mwhc_out import mwhc_out
from omg.cmd.get.pv_out import pv_out
from omg.cmd.get.sc_out import sc_out
from omg.cmd.get.secret_out import secret_out
from omg.cmd.get.service_out import service_out
from omg.cmd.get.route_out import route_out
from omg.cmd.get.cm_out import cm_out
from omg.cmd.get.ep_out import ep_out
from omg.cmd.get.ev_out import ev_out
from omg.cmd.get.deployment_out import deployment_out
from omg.cmd.get.rs_out import rs_out
from omg.cmd.get.ss_out import ss_out
from omg.cmd.get.vwhc_out import vwhc_out
from omg.cmd.get.machine_out import machine_out
from omg.cmd.get.machineset_out import machineset_out


# This map and function normalizes/standarizes the different names of object/resources types
# Also returns the function that handles get,describe and output of this object type
# This is how the top level get_main function knows which objects we can handle and how.
# returns None if not an object type that we can't handle


map = [
    {   'type': 'pod','aliases': ['pods', 'po'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': pod_out,
        'yaml_loc': 'namespaces/%s/core/pods.yaml' },

    {   'type': 'service','aliases': ['services', 'svc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': service_out,
        'yaml_loc': 'namespaces/%s/core/services.yaml' },

    {   'type': 'secret','aliases': ['secrets'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': secret_out,
        'yaml_loc': 'namespaces/%s/core/secrets.yaml' },

    {   'type': 'configmap','aliases': ['configmaps', 'cm'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': cm_out,
        'yaml_loc': 'namespaces/%s/core/configmaps.yaml' },

    {   'type': 'endpoint','aliases': ['endpoints', 'ep'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': ep_out,
        'yaml_loc': 'namespaces/%s/core/endpoints.yaml' },

    {   'type': 'event','aliases': ['events', 'ev'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': ev_out,
        'yaml_loc': 'namespaces/%s/core/events.yaml' },

    {   'type': 'persistentvolumeclaim','aliases': ['persistentvolumeclaims', 'pvc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'namespaces/%s/core/persistentvolumeclaims.yaml' }, ###

    {   'type': 'replicationcontroller','aliases': ['replicationcontrollers', 'rc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'namespaces/%s/core/replicationcontrollers.yaml' }, ###

    {   'type': 'replicaset','aliases': ['replicasets', 'rs'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': rs_out,
        'yaml_loc': 'namespaces/%s/apps/replicasets.yaml' },

    {   'type': 'statefulset','aliases': ['statefulsets'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': ss_out,
        'yaml_loc': 'namespaces/%s/apps/statefulsets.yaml' }, ###

    {   'type': 'deployment','aliases': ['deployments'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': deployment_out,
        'yaml_loc': 'namespaces/%s/apps/deployments.yaml' },
    
    {   'type': 'daemonset','aliases': ['daemonsets', 'ds'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'namespaces/%s/apps/daemonsets.yaml' }, ###

    {   'type': 'deploymentconfig','aliases': ['deploymentconfigs', 'dc'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'namespaces/%s/apps.openshift.io/deploymentconfigs.yaml' }, ###

    {   'type': 'route','aliases': ['routes'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': route_out,
        'yaml_loc': 'namespaces/%s/route.openshift.io/routes.yaml' }, ###

    {   'type': 'node','aliases': ['nodes'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': node_out,
        'yaml_loc': 'cluster-scoped-resources/core/nodes' },
        # When yaml_loc is a dir like in this case, we scan *.yaml files in it.

    {   'type': 'persistentvolume','aliases': ['persistentvolumes', 'pv'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': pv_out,
        'yaml_loc': 'cluster-scoped-resources/core/persistentvolumes' },

    {   'type': 'machineconfigpool','aliases': ['machineconfigpools', 'mcp'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': mcp_out,
        'yaml_loc': 'cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigpools' },

    {   'type': 'machineconfig','aliases': ['machineconfigs', 'mc'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': mc_out,
        'yaml_loc': 'cluster-scoped-resources/machineconfiguration.openshift.io/machineconfigs' },

    {   'type': 'apiserver','aliases': ['apiservers'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/apiservers.yaml' },

    {   'type': 'authentication','aliases': ['authentications'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/authentications.yaml' },

    {   'type': 'clusteroperator','aliases': ['clusteroperators', 'co'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': co_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/clusteroperators.yaml' },

    {   'type': 'clusterversion','aliases': ['clusterversions'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': cv_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/clusterversions.yaml' },

    {   'type': 'console','aliases': ['consoles'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/consoles.yaml' },

    {   'type': 'certificatesigningrequest','aliases': ['certificatesigningrequests', 'csr'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': csr_out,
        'yaml_loc': 'cluster-scoped-resources/certificates.k8s.io/certificatesigningrequests' },

    {   'type': 'dns','aliases': ['dnses'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/dnses.yaml' },

    {   'type': 'featuregate','aliases': ['featuregates'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/featuregates.yaml' },

    {   'type': 'image','aliases': ['images'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/images.yaml' },

    {   'type': 'infrastructure','aliases': ['infrastructures'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/infrastructures.yaml' },

    {   'type': 'ingress','aliases': ['ingresses'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/ingresses.yaml' },

    {   'type': 'mutatingwebhookconfiguration','aliases': ['mutatingwebhookconfigurations'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': mwhc_out,
        'yaml_loc': 'cluster-scoped-resources/admissionregistration.k8s.io/mutatingwebhookconfigurations' },

    {   'type': 'network','aliases': ['networks'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/networks.yaml' },

    {   'type': 'oauth','aliases': ['oauths'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/oauths.yaml' },

    {   'type': 'operatorhub','aliases': ['operatorhubs'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/operatorhubs.yaml' },

    {   'type': 'project','aliases': ['projects'],'need_ns': False,
        'get_func': get_project, 'getout_func': project_out,
        'yaml_loc': 'namespaces/*/*.yaml' },

    {   'type': 'proxy','aliases': ['proxies'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/proxies.yaml' },

    {   'type': 'scheduler','aliases': ['schedulers'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/config.openshift.io/schedulers.yaml' },

    {   'type': 'storageclass','aliases': ['storageclasses', 'sc'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': sc_out,
        'yaml_loc': 'cluster-scoped-resources/storage.k8s.io/storageclasses' },

    {   'type': 'validatingwebhookconfiguration','aliases': ['validatingwebhookconfigurations'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': vwhc_out,
        'yaml_loc': 'cluster-scoped-resources/admissionregistration.k8s.io/validatingwebhookconfigurations' },

    {   'type': 'machineset','aliases': ['machinesets'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': machineset_out,
        'yaml_loc': 'namespaces/%s/machine.openshift.io/machinesets' },

    {   'type': 'machine','aliases': ['machines'],'need_ns': True,
        'get_func': from_yaml, 'getout_func': machine_out,
        'yaml_loc': 'namespaces/%s/machine.openshift.io/machines' },

    {   'type': 'customresourcedefinition','aliases': ['customresourcedefinitions', 'crd', 'crds'],'need_ns': False,
        'get_func': from_yaml, 'getout_func': simple_out,
        'yaml_loc': 'cluster-scoped-resources/apiextensions.k8s.io/customresourcedefinitions' },

]


def map_res(t):
    if t is not None:
        for x in map:
            # match the input with type: or alias (without case)
            if t.lower() == x['type'].lower() or t.lower() in [y.lower() for y in x['aliases'] ]:
                return x
    return None
