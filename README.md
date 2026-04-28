apt-get update && apt-get install bind bind-utils -y

echo $'search au-team.irpo\nnameserver 127.0.0.1' > /etc/net/ifaces/enp7s1/resolv.conf

rndc-confgen -a -c /etc/bind/rndc.key


nano /etc/bind/options.conf

options {
    listen-on { 127.0.0.1; 192.168.100.2; };
    forwarders { 77.88.8.7; 77.88.8.3; };
    recursion yes;
    allow-recursion { any; };
    allow-query { any; };
    dnssec-validation no;
    directory "/etc/bind/zone";
    dump-file "/var/run/named/named_dump.db";
    statistics-file "/var/run/named/named.stats";
    pid-file "/var/run/named/named.pid";
};

logging {
    category default { default_syslog; };
};

zone "au-team.irpo" {
    type master;
    file "au-team.irpo";
};

zone "168.192.in-addr.arpa" {
    type master;
    file "168.192.in-addr.arpa";
};





==========================================
nano /etc/bind/zone/au-team.irpo

$TTL 1D
@ IN SOA au-team.irpo. root.au-team.irpo. (
	2025020600
    12H
    1H
    1W
    1H
)
@       IN NS    hq-srv.au-team.irpo.

hq-rtr  IN A     192.168.100.1
hq-srv  IN A     192.168.100.2
hq-cli  IN A     192.168.200.2
br-rtr  IN A     192.168.1.1
br-srv  IN A     192.168.1.2
docker  IN A     172.16.1.1
web     IN A     172.16.2.1






==========================================
nano /etc/bind/zone/168.192.in-addr.arpa

$TTL 1D
@ IN SOA au-team.irpo. root.au-team.irpo. (
    2025020600
    12H
    1H
    1W
    1H
)
@       IN NS    au-team.irpo.

1.100   IN PTR   hq-rtr.au-team.irpo.
2.100   IN PTR   hq-srv.au-team.irpo.
2.200   IN PTR   hq-cli.au-team.irpo.





==========================================

chown :named /etc/bind/zone/au-team.irpo /etc/bind/zone/168.192.in-addr.arpa

systemctl enable --now bind

service network restart

host br-rtr

host -t PTR 192.168.100.2


-
rm -f /etc/net/ifaces/enp7s1/resolv.conf

echo $'search au-team.irpo\nnameserver 192.168.100.2' > /etc/net/ifaces/vlan100/resolv.conf



sed -i 's/AUTO_LOCAL_RESOLVER=yes/AUTO_LOCAL_RESOLVER=no/' /etc/sysconfig/dnsmasq ; grep AUTO_LOCAL_RESOLVER /etc/sysconfig/dnsmasq

nano /etc/dnsmasq.conf

port=0
interface=vlan200
listen-address=192.168.200.1
dhcp-authoritative
dhcp-range=interface:vlan200,192.168.200.2,192.168.200.2,255.255.255.240,6h
dhcp-option=3,192.168.200.1
dhcp-option=6,192.168.100.2
leasefile-ro





systemctl enable --now dnsmasq ; ss -lun | grep 67

systemctl restart network

cat /etc/resolv.conf
