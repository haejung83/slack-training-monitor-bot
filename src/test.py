import subprocess
import asyncio
print('run test')

p = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE)
poll = p.poll();
print("before wait %s" %(poll))
print("return code %s" %(p.returncode))

p.wait()

poll = p.poll();
print("after wait %s" %(poll))
print("return code %s" %(p.returncode))

print("OUTPUT: %s" %(p.stdout.read().decode('utf-8')))


async def test_loop():
    print('test1')
    await asyncio.sleep(0.1)
    print('test1 after')


async def test_loop2():
    print('test2')
    await asyncio.sleep(0.9)
    print('test2 after')

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

tasks = [asyncio.ensure_future(test_loop()), asyncio.ensure_future(test_loop2())]

loop.run_until_complete(asyncio.gather(*tasks))
