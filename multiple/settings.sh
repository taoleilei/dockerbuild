#!/bin/bash
#
 
cat >> /etc/security/limits.conf <<EOF
*           soft   nofile       288000
*           hard   nofile       288000
*           soft   nproc        288000
*           hard   nproc        288000
*           soft  memlock      unlimited
*           hard  memlock      unlimited
root        soft   nofile       288000
root        hard   nofile       288000
root        soft   nproc        288000
root        hard   nproc        288000
root        soft  memlock      unlimited
root        hard  memlock      unlimited
EOF

cat >> /etc/pam.d/common-session <<EOF
session required        pam_limits.so
EOF

cat >> /etc/profile <<EOF
ulimit -SHn 288000
EOF

cat >> /etc/sysctl.conf <<EOF
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_max_syn_backlog = 102400
fs.file-max = 288000
net.core.somaxconn = 102400
EOF

/sbin/sysctl -p