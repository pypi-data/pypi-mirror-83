import time

import ovirtsdk4 as sdk
import ovirtsdk4.types as types


class BaseRhvAPI:
    """simple wrapper for oVirt sdk"""

    def __init__(self, url: str,
                 credential: tuple = ('admin@internal', 'password')):
        self.url = url
        self.credential = credential
        self.conn = sdk.Connection(url=self.url,
                                   username=self.credential[0],
                                   password=self.credential[1],
                                   insecure=True)

        self.dcs_srv = self.conn.system_service().data_centers_service()
        self.clusters_srv = self.conn.system_service().clusters_service()
        self.hosts_srv = self.conn.system_service().hosts_service()
        self.vms_srv = self.conn.system_service().vms_service()
        self.sds_srv = self.conn.system_service().storage_domains_service()
        self.nws_srv = self.conn.system_service().networks_service()
        self.events_srv = self.conn.system_service().events_service()

        self.cluster_lv_srv = self.conn.system_service().cluster_levels_service()

    def _debug(self):
        clv = self.cluster_lv_srv.level_service('4.4')
        for cpu in clv.get().cpu_types:
            print(cpu.name)

    # =========================================================
    # ================ Data Center Operations =================
    # =========================================================
    def add_data_center(self, name, **kwargs):
        """create datacenter with local storage, and wait for the reponse
        >>> api = BaseRhvAPI("https://vm-198-170.lab.eng.pek2.redhat.com/ovirt-engine/api")
        >>> api.add_data_center("dc_name", local=False, wait=True, major_ver=4, minor_ver=4)
        """
        try:
            dc = self.dcs_srv.add(types.DataCenter(
                name=name,
                local=kwargs.get('local'),
                version=types.Version(
                    major=kwargs.get('major_ver'),
                    minor=kwargs.get('minor_ver'))
            ), wait=True)
            return dc.id
        except sdk.Error as e:
            if 'already in use' in e.fault.detail:
                print(e.fault.detail)
                # TODO try to delete first
            else:
                raise e

    def find_data_center(self, name) -> str:
        results = self.dcs_srv.list(search=f"name={name}")
        if len(results) != 1:
            raise RuntimeError(f"can't find data_center {name}")
        return results[0].id

    def del_data_center(self, name):
        dc_id = self.find_data_center(name)
        dc = self.dcs_srv.data_center_service(dc_id)
        dc.remove(force=True, wait=True)

    # =========================================================
    # ================ Cluster Operations =====================
    # =========================================================
    def add_cluster(self, name: str, **kwargs) -> str:
        cpu_type = kwargs.get('cpu_type')
        cluster_level = kwargs.get('cluster_level', '4.4')
        major_ver, minor_ver = cluster_level.split('.')
        if cpu_type not in self.cluster_supported_cpu_types(level=cluster_level):
            raise RuntimeError(f"{cpu_type} is not on supported list")

        try:
            cluster = self.clusters_srv.add(
                types.Cluster(
                    name=name,
                    cpu=types.Cpu(
                        architecture=types.Architecture.X86_64,  # TODO hard code cpu arch here
                        type=kwargs.get('cpu_type')  # e.g.: Intel Conroe Family
                    ),
                    data_center=types.DataCenter(
                        name=kwargs.get('data_center_name')
                    ),
                    version=types.Version(major=major_ver, minor=minor_ver),
                    management_network=types.Network(name=kwargs.get("nw_name", "ovirtmgmt"))
                ), wait=True
            )
            return cluster.id
        except sdk.Error as e:
            print(e.fault.detail)

    def find_cluster(self, name: str):
        results = self.clusters_srv.list(search=f"name={name}")
        if len(results) != 1:
            raise RuntimeError(f"can't find cluster {name}")
        return results[0].id

    def del_cluster(self, name: str):
        cluster_id = self.find_cluster(name)
        cluster = self.clusters_srv.cluster_service(cluster_id)
        return cluster.remove(wait=True)

    def cluster_supported_cpu_types(self, level: str) -> list:
        clv = self.cluster_lv_srv.level_service(level)
        return [cpu.name for cpu in clv.get().cpu_types]

    # =========================================================
    # ================ Host Operations ========================
    # =========================================================
    def add_host(self, name: str, **kwargs) -> str:
        host = self.hosts_srv.add(
            types.Host(
                name=name,
                address=kwargs.get('address'),
                root_password=kwargs.get('root_password'),
                cluster=types.Cluster(
                    name=kwargs.get('cluster_name')
                ),
            ),
            deploy_hosted_engine=kwargs.get('deploy_hosted_engine'),
            wait=True
        )
        # wait till host is up
        host_srv = self.hosts_srv.host_service(host.id)
        begin = time.time()
        while True:
            time.sleep(10)
            host = host_srv.get()
            print(f"waiting for host {name} up, {time.time() - begin}")
            if host.status == types.HostStatus.UP:
                break
        return host.id

    def find_host(self, name: str) -> str:
        results = self.hosts_srv.list(search=f"name={name}")
        if len(results) != 1:
            raise RuntimeError(f"can't find host {name}")
        return results[0].id

    def del_host(self, name: str):
        host_id = self.find_host(name)
        host = self.hosts_srv.host_service(host_id)
        return host.remove(force=True, wait=True)

    def activate_host(self, name: str):
        host_id = self.find_host(name)
        host = self.hosts_srv.host_service(host_id)
        return host.activate()

    def deactivate_host(self, name: str):
        """Deactivates the host to perform maintenance tasks"""
        host_id = self.find_host(name)
        host = self.hosts_srv.host_service(host_id)
        return host.deactivate()

    def check_host_upgrade(self, name: str) -> bool:
        host_id = self.find_host(name)
        host_srv = self.hosts_srv.host_service(host_id)
        host = host_srv.get()

        if host.update_available:
            print(f"Host {name} has update")
            return True
        else:
            print(f"Host {name} has no update")
            return False

    def upgrade_host(self, name: str, **kwargs):
        host_id = self.find_host(name)
        host = self.hosts_srv.list(search=f"name={name}")[0]
        host_srv = self.hosts_srv.host_service(host_id)

        if not host.update_available:
            host_srv.upgrade_check()

            last_event = self.events_srv.list(max=1)[0]
            timeout = 300
            while timeout > 0:
                events = [
                    event.code for event in self.events_srv.list(
                        from_=int(last_event.id),
                        search='host.name=%s' % host.name,
                    )
                ]
                if 839 in events or 887 in events:
                    print(f"Check for host {name} upgrade failed.")
                    break
                if 885 in events:
                    print(f"Check for host {name} upgrade done.")
                    break
                time.sleep(2)
                timeout = timeout - 2

        host = host_srv.get()
        if host.update_available:
            print(f"Host {name} start upgrading")
            host_srv.upgrade()

    def current_host_status(self, name: str) -> str:
        host_id = self.find_host(name)
        host = self.hosts_srv.host_service(host_id).get()
        return host.status

    # =========================================================
    # ================ Virtual Machine Operations =============
    # =========================================================
    def add_vm(self, name: str, **kwargs):
        vm = self.vms_srv.add(types.Vm(
            name=name,
            cluster=types.Cluster(
                name=kwargs.get('cluster_name')
            ),
            template=types.Template(
                name=kwargs.get("template_name")
            )
        ), wait=True)
        return vm

    def find_vm(self, name: str):
        results = self.vms_srv.list(search=f"name={name}")
        if len(results) != 1:
            raise RuntimeError(f"can't find vm {name}")
        return results[0].id

    def start_vm(self, name: str):
        """start a vm, for easy testing, boot from CDROM only"""

        vm_id = self.find_vm(name)
        vm_srv = self.vms_srv.vm_service(vm_id)
        vm_srv.start(vm=types.Vm(
            os=types.OperatingSystem(
                boot=types.Boot(
                    devices=[
                        types.BootDevice.CDROM,
                        types.BootDevice.NETWORK
                    ]
                )
            )
        ))

        while True:
            time.sleep(5)
            vm = vm_srv.get()
            print(f"wait for vm:{name} up")
            if vm.status == types.VmStatus.UP:
                print(f"vm:{name} is up")
                break

    def stop_vm(self, name: str):
        vm_id = self.find_vm(name)
        vm_srv = self.vms_srv.vm_service(vm_id)
        vm_srv.stop()

        while True:
            time.sleep(5)
            vm = vm_srv.get()
            print(f"wait for vm:{name} down")
            if vm.status == types.VmStatus.DOWN:
                print(f"vm:{name} is down")
                break

    def del_vm(self, name: str):
        vm_id = self.find_vm(name)
        vm = self.vms_srv.vm_service(vm_id)
        return vm.remove(force=True)

    def migrate_vm(self, vm_name: str, host_name: str):
        vm_id = self.find_vm(vm_name)
        vm_srv = self.vms_srv.vm_service(vm_id)
        vm_srv.migrate(host=types.Host(name=host_name))

        while True:
            time.sleep(5)
            vm = vm_srv.get()
            if vm.status == types.VmStatus.MIGRATING:
                print(f"vm:{vm_name} is migrating")
                continue
            if vm.status == types.VmStatus.UP:
                print(f"vm:{vm_name} is UP, migrating done")
                break

    # ================ NFS Storage Operations =====================
    # =============================================================
    def add_nfs_storage(self, name: str, **kwargs):
        """this method add nfs storage in UNATTACHED status"""
        sd = self.sds_srv.add(
            types.StorageDomain(
                name=name,
                type=types.StorageDomainType.DATA,
                host=types.Host(
                    name=kwargs.get('host_name'),
                ),
                storage=types.HostStorage(
                    type=types.StorageType.NFS,
                    address=kwargs.get('nfs_address'),
                    path=kwargs.get('nfs_path'),
                )
            ),
        )

        sd_service = self.sds_srv.storage_domain_service(sd.id)
        now = time.time()
        while True:
            time.sleep(5)
            sd = sd_service.get()
            print(f"wait for NFS storage ready, {time.time() - now}")
            if sd.status == types.StorageDomainStatus.UNATTACHED:
                break

        print(f"start to attach storage:{name} to data-center:{kwargs.get('dc_name')}")
        self.attach_storage_to_data_center(name, kwargs.get('dc_name'))

    def attach_storage_to_data_center(self, storage_name: str, data_center_name: str):
        """attach unattached storage to specific datacenter"""

        sd_id = self.find_nfs_storage(storage_name)
        dc_id = self.find_data_center(data_center_name)
        dc = self.dcs_srv.data_center_service(dc_id)

        attached_sds_service = dc.storage_domains_service()
        attached_sds_service.add(
            types.StorageDomain(
                id=sd_id
            )
        )

        attached_sd_service = attached_sds_service.storage_domain_service(sd_id)
        now = time.time()
        while True:
            time.sleep(10)
            print(f"wait for storage:{storage_name} UP -- {time.time() - now}")
            sd = attached_sd_service.get()
            if sd.status == types.StorageDomainStatus.ACTIVE:
                break

    def find_nfs_storage(self, name):
        results = self.sds_srv.list(search=f"name={name}")
        if len(results) != 1:
            raise RuntimeError(f"can't find nfs storage {name}")
        return results[0].id

    def del_nfs_storage(self, name: str, **kwargs):
        sd_id = self.find_nfs_storage(name)
        sd = self.sds_srv.storage_domain_service(sd_id)
        sd.remove(host=kwargs.get('host_name'), format=True)

    # ================ iSCSI Storage Operations =====================
    # =============================================================
    def add_iscsi_storage(self, name, **kwargs):
        sd = self.sds_srv.add(
            types.StorageDomain(
                name=name,
                description="iSCSI without discard after delete",
                type=types.StorageDomainType.DATA,
                discard_after_delete=False,
                data_center=types.DataCenter(name=kwargs.get("data_center_name")),
                host=types.Host(name=kwargs.get("host_name")),
                storage_format=types.StorageFormat.V5,
                storage=types.HostStorage(
                    type=types.StorageType.ISCSI,
                    override_luns=True,
                    volume_group=types.VolumeGroup(
                        logical_units=[
                            types.LogicalUnit(
                                id=kwargs.get("lun_id"),
                                address=kwargs.get("address"),
                                port=kwargs.get("port"),
                                target=kwargs.get("target")
                            )
                        ]
                    )
                )
            )
        )

        dc = self.dcs_srv.list(search=f"name={kwargs.get('data_center_name')}")[0]
        dc_srv = self.dcs_srv.data_center_service(dc.id)

        attached_sds_service = dc_srv.storage_domains_service()

        attached_sds_service.add(
            types.StorageDomain(
                id=sd.id,
            ),
        )

        attached_sd_service = attached_sds_service.storage_domain_service(sd.id)

        now = time.time()
        while True:
            time.sleep(10)
            sd = attached_sd_service.get()
            print(f"wait for iSCSI storage up, {time.time() - now}")
            if sd.status == types.StorageDomainStatus.ACTIVE:
                break

    # =========================================================
    # ================ Network Operations =====================
    # =========================================================
    def add_network(self, name: str, dc_name: str, **kwargs):
        return self.nws_srv.add(
            network=types.Network(
                name=name,
                data_center=types.DataCenter(
                    name=dc_name
                ),
                vlan=types.Vlan(id=kwargs.get("vlan_id")),
                usages=[types.NetworkUsage.VM],
                mtu=1500,
            )
        )

    def find_network(self, dc_name: str, nw_name: str):
        dc_id = self.find_data_center(dc_name)
        dc_srv = self.dcs_srv.data_center_service(dc_id)
        nw_srvs = dc_srv.networks_service()
        networks = nw_srvs.list(search=f"name={nw_name}")

        if len(networks) != 1:
            raise RuntimeError("can't find network")
        return networks[0].id

    def update_network(self,
                       dc_name: str,
                       nw_name: str = "ovirtmgmt",
                       vlan_id: str = "50", **kwargs):

        vlan = types.Vlan(id=vlan_id)

        nw_id = self.find_network(dc_name, nw_name=nw_name)
        nw = self.nws_srv.network_service(nw_id)
        return nw.update(types.Network(
            vlan=vlan,
            id=nw_id))
