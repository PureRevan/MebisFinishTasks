from WebDriverPy.driver import WebDriver, By, WebDriverWait
from sys import argv


HEADLESS = False


if __name__ == '__main__':
    if len(argv) > 1 and argv[1] in ["--headless", "-h", "--h"]:
        HEADLESS = True

    driver = WebDriver(
        no_cookies=False,
        use_ad_blocker=False,
        try_spoofing=True,
        keyboard_spoofing=False,
        headless=HEADLESS,
        late_init=True
    )

    user = ""
    while not user:
        user = driver.get_user_input("Mebis Benutzername: ").strip()

    pwd = ""
    while not pwd:
        pwd = driver.get_user_input("Mebis Passwort: ").strip()
    print()

    driver.init()
    driver.get("https://lernplattform.mebis.bycs.de")
    driver.wait_click_write(user, "input-username", timeout=10)
    driver.wait_click_write(pwd, "input-password", timeout=10)
    driver.wait_and_click("button-do-log-in", timeout=10)

    driver.wait_for_user_input("Bitte navigieren Sie zur entsprechenden Kursseite und drücken Sie dann Enter...")

    target_base = ""
    print("Kopieren Sie die Addresse eines Link und fügen Sie dann ihn hier ein")
    print("Der Link sollte ungefähr so aussehen: https://lernplattform.mebis.bycs.de/mod/resource/view.php?id=12345678")
    print()
    while not target_base:
        target_base = driver.get_user_input("Link: ").strip()

    anchors = driver.wait_and_find(
        f"//a[@href='{target_base}']/ancestor::ul[1]",
        "XPATH",
        timeout=10
    ).find_elements(By.XPATH, ".//a[@href]")

    links = [href for a in anchors if (href := a.get_attribute("href")) and href != target_base]

    original_window = driver.current_window_handle

    for link in links:
        driver.execute_script("window.open(arguments[0], '_blank');", link)

    print("Auf das Laden der Seiten warten (5 Sekunden)...")
    driver.wait(5)

    for handle in driver.window_handles:
        if handle == original_window:
            continue

        driver.switch_to.window(handle)

        driver.wait_until(
            lambda d: d.execute_script("return document.readyState") == "complete",
            timeout=10
        )

    driver.switch_to.window(original_window)
    driver.refresh()
    driver.wait(1)

    print()
    print("Alle durch Laden von Seiten erledigbaren Aufgaben sollten erledigt worden sein.")

    close = driver.get_user_input("Sollen die anderen Tabs geschlossen werden? [y/N]").lower() == "y"

    if close:
        try:
            for handle in driver.window_handles:
                if handle != original_window:
                    driver.switch_to.window(handle)
                    driver.close()
        except Exception:
            pass
    
    print()
    driver.wait_for_user_input("Fertig...")
    driver.close()
