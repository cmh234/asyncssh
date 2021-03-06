#!/usr/bin/env python3.5
#
# Copyright (c) 2013-2017 by Ron Frederick <ronf@timeheart.net>.
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

import asyncio, asyncssh, sys, time

passwords = {'guest': '',                 # guest account with no password
             'user123': 'test'   # password of 'secretpw'
            }

def handle_client(process):
    process.stdout.write('Welcome to my SSH server, %s!\n' %
                         process.channel.get_extra_info('username'))
    process.stdout.write('Put code here to do something until then I quit, %s!\n' %
                         process.channel.get_extra_info('username'))

    process.exit(0)

class MySSHServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        print('SSH connection received from %s.' %
                  conn.get_extra_info('peername')[0])

    def connection_lost(self, exc):
        if exc:
            print('SSH connection error: ' + str(exc), file=sys.stderr)
        else:
            print('SSH connection closed.')

    def begin_auth(self, username):
        # If the user's password is the empty string, no auth is required
        return passwords.get(username) != ''

    def password_auth_supported(self):
        return True

    def validate_password(self, username, password):
        pw = passwords.get(username, '*')
        #return crypt.crypt(password, pw) == pw
        #return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) == pw
        return password == pw



async def start_server():
    port = 8022
    ip = '0.0.0.0'
    ssh_host_key = 'flask_app/asyncssh/keys/mysshkey'
    await asyncssh.create_server(MySSHServer, '', 8022,
                                 server_host_keys=[ssh_host_key],
                                 process_factory=handle_client)
    print(time.strftime("%Y-%m-%d %H:%M"))
    print("Server started at: {0}:{1}".format(ip, port))


loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(start_server())
except (OSError, asyncssh.Error) as exc:
    sys.exit('Error starting server: ' + str(exc))

loop.run_forever()
