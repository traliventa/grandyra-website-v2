import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    name=sys.argv[1]; w=int(sys.argv[2]); h=int(sys.argv[3]); steps=[int(x) for x in sys.argv[4].split(',')]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--use-gl=swiftshader','--enable-unsafe-swiftshader'])
        ctx=await b.new_context(viewport={'width':w,'height':h})
        pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e: errs.append(str(e)))
        pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
        await pg.goto(f'http://127.0.0.1:8765/{name}.html'); await pg.wait_for_timeout(3800)
        await pg.mouse.move(w*0.5,h*0.45)
        y=0
        for i,s in enumerate(steps):
            await pg.mouse.wheel(0,s-y); y=s
            await pg.wait_for_timeout(1700)
            await pg.screenshot(path=f'shots/{name}-{w}-{i}.png')
        ow=await pg.evaluate('document.documentElement.scrollWidth>innerWidth+1')
        print(name,w,'overflow' if ow else 'ok',errs[:5])
        await b.close()
asyncio.run(main())
