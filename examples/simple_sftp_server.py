#!/usr/bin/env python3.5
#
# Copyright (c) 2015-2016 by Ron Frederick <ronf@timeheart.net>.
# All rights reserved.
#
# This program and the accompanying materials are made available under
# the terms of the Eclipse Public License v1.0 which accompanies this
# distribution and is available at:
#
#     http://www.eclipse.org/legal/epl-v10.html
#
# Contributors:
#     Ron Frederick - initial implementation, API, and documentation

# To run this program, the file ``ssh_host_key`` must exist with an SSH
# private key in it to use as a server host key. An SSH host certificate
# can optionally be provided in the file ``ssh_host_key-cert.pub``.
#
# The file ``ssh_user_ca`` must exist with a cert-authority entry of
# the certificate authority which can sign valid client certificates.

import asyncio, asyncssh, sys, time, os


port = 8022
ip = '0.0.0.0'
ssh_host_key = 'flask_app/asyncssh/keys/mysshkey'
ssh_user_ca = 'flask_app/asyncssh/keys/pubkey_openSsh.pub'


class MySFTPServer(asyncssh.SFTPServer):
    def __init__(self, conn):
        root = '/tmp/sftp/' + conn.get_extra_info('username')
        os.makedirs(root, exist_ok=True)
        super().__init__(conn, chroot=root)

async def start_server():
    await asyncssh.listen('', port, server_host_keys=[ssh_host_key],
                          authorized_client_keys=ssh_user_ca,
                          sftp_factory=MySFTPServer)

loop = asyncio.get_event_loop()
print(time.strftime("%Y-%m-%d %H:%M"))
print("Server started at: {0}:{1}".format(ip, port))

try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))

loop.run_forever()
