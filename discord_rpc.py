import discordrpc

rpc = discordrpc.RPC(app_id=1217556150325743757)

def setrpc(song):
    rpc.set_activity(
        state=f"Playing song: {song}",
)

def startrpc():
    rpc.run