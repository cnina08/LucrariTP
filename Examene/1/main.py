from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

# Partea 1: apeluri pentru build_url și is_https
print(" Partea 1 ")
print("Partea 1, build_url (fără /):", build_url("example.com", "login"))
print("Partea 1, build_url (cu /):", build_url("example.com", "/login"))
print("Partea 1, is_https (HTTPS):", is_https("https://example.com"))
print("Partea 1, is_https (HTTP):", is_https("http://example.com"))

# Partea 2: apeluri pentru show_response
print("\n Partea 2")
print("Partea 2, show_response pentru https://example.com:")
show_response("https://example.com")
print("Partea 2, show_response pentru URL invalid:")
show_response("http://site-inexistent.invalid")

# Partea 3: apeluri pentru check_site
print("\n Partea 3")
print("Partea 3, check_site (succes):", check_site("https://example.com"))
print("Partea 3, check_site (eșec/inexistent):", check_site("http://site-inexistent.invalid"))

# Partea 4: apelul scan_sites()
print("\n Partea 4 ")
scan_sites()

# Partea 5: apeluri pentru check_headers
print("\n Partea 5 ")
print("Partea 5, check_headers (example.com):", check_headers("https://example.com"))
print("Partea 5, check_headers (httpbin headers):", check_headers("https://httpbin.org/headers"))

# Partea 6: apeluri pentru retry_check
print("\nPartea 6 ")
print("Partea 6, retry_check 200:", retry_check("https://httpbin.org/status/200"))
print("Partea 6, retry_check 404:", retry_check("https://httpbin.org/status/404"))
print("Partea 6, retry_check 500:", retry_check("https://httpbin.org/status/500"))
print("Partea 6, retry_check invalid:", retry_check("http://site-inexistent.invalid"))