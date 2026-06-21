import sys
import json
import asyncio
from playwright.async_api import async_playwright

async def get_shopee_product(url):
    result = {"success": False, "title": "", "description": "", "error_type": "", "error": ""}
    async with async_playwright() as p:
        try:
            print("Connecting to Chrome via CDP (http://localhost:9222)...", file=sys.stderr)
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            context = browser.contexts[0]
            page = await context.new_page()
            
            print(f"Navigating to Shopee: {url}...", file=sys.stderr)
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Beri jeda 4 detik agar konten selesai dirender oleh JS Shopee
            await page.wait_for_timeout(4000)
            
            # 1. Ekstrak judul produk
            title = await page.title()
            if " | Shopee Indonesia" in title:
                title = title.replace(" | Shopee Indonesia", "")
            
            # 2. Ekstrak deskripsi dari JSON-LD
            description = ""
            ld_json_scripts = await page.query_selector_all('script[type="application/ld+json"]')
            for script in ld_json_scripts:
                try:
                    text = await script.text_content()
                    data = json.loads(text)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        if item.get("@type") == "Product" or "description" in item:
                            if item.get("description") and len(item["description"].strip()) > 10:
                                description = item["description"].strip()
                                break
                except Exception:
                    pass
                if description:
                    break
                    
            # 3. Fallback jika deskripsi masih kosong
            if not description:
                pre_wraps = await page.evaluate("""() => {
                    const els = Array.from(document.querySelectorAll('div, p, span, section'))
                        .filter(el => {
                            if (el.closest('div.product-ratings') || el.closest('header') || el.closest('footer') || el.closest('[class*="rating"]')) return false;
                            const style = window.getComputedStyle(el);
                            return (style.whiteSpace.includes('pre-wrap') || style.whiteSpace.includes('pre-line')) && el.textContent.trim().length > 100;
                        });
                    if (els.length > 0) {
                        els.sort((a, b) => b.textContent.trim().length - a.textContent.trim().length);
                        return els[0].textContent.trim();
                    }
                    return '';
                }""")
                if pre_wraps:
                    description = pre_wraps
                    
            if not description:
                detail_sec = await page.query_selector('div[class*="product-detail"]')
                if detail_sec:
                    description = await detail_sec.inner_text()
                    description = description.strip()
            
            await page.close()
            
            current_url = page.url
            is_blocked = False
            if "Situs Belanja Online Terlengkap" in title or "shopee.co.id" == current_url.strip("/").split("?")[0].replace("https://", "").replace("www.", ""):
                is_blocked = True
            if "buyer/login" in current_url or "universal-link" in current_url:
                is_blocked = True
                
            if is_blocked or not description:
                result = {
                    "success": False,
                    "error_type": "verification_required",
                    "error": "Terdeteksi verifikasi/login Shopee pada browser Chrome. Silakan buka browser Chrome Anda, masuk ke akun Shopee, lalu coba lagi."
                }
            else:
                result = {
                    "success": True,
                    "title": title,
                    "description": description
                }
        except Exception as e:
            err_msg = str(e)
            print(f"Error during CDP execution: {err_msg}", file=sys.stderr)
            if "connect_over_cdp" in err_msg or "Failed to connect" in err_msg or "Target page, context or browser has been closed" in err_msg:
                result["error_type"] = "cdp_closed"
                result["error"] = "Gagal terhubung ke Chrome. Pastikan Anda sudah menjalankan Chrome dengan perintah: google-chrome --remote-debugging-port=9222"
            else:
                result["error_type"] = "exception"
                result["error"] = f"Terjadi kesalahan saat mengambil data Shopee: {err_msg}"
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "error": "No URL disediakan"}))
        sys.exit(1)
    url_arg = sys.argv[1]
    res = asyncio.run(get_shopee_product(url_arg))
    print(json.dumps(res))
