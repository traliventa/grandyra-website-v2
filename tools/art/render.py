import asyncio, base64, io
from playwright.async_api import async_playwright
from PIL import Image
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome')
        pg=await b.new_page()
        await pg.goto(''+'file://'+__import__('os').path.abspath(__import__('os').path.join(__import__('os').path.dirname(__file__),'art.html'))+'')
        await pg.evaluate('document.fonts.load("italic 100px Bod")'); await pg.evaluate('document.fonts.load("800 100px Arc")')
        await pg.wait_for_timeout(500)
        jobs=await pg.evaluate('window.JOBS')
        for j in jobs:
            data=await pg.evaluate(f'window.render("{j}")')
            im=Image.open(io.BytesIO(base64.b64decode(data.split(',')[1]))).convert('RGB')
            if j.startswith('og'):
                im.resize((1200,630)).save(f'site/assets/img/{j}.jpg',quality=86)
            else:
                im.save(f'site/assets/img/{j}.webp',quality=82)
                im.resize((800,600)).save(f'site/assets/img/{j}-sm.webp',quality=80)
        await b.close()
        print(len(jobs),'images')
asyncio.run(main())
