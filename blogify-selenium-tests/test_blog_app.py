import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:9090"  # Change this if your local server runs on a different port

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")  # Run browser in background
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# 1. Homepage title test
def test_homepage_title(driver):
    driver.get(BASE_URL)
    assert "Homepage" in driver.title

# 2. Signup user
def test_signup_user(driver):
    driver.get(f"{BASE_URL}/user/signup")
    driver.find_element(By.ID, "fullName").send_keys("Iman Selenium")
    driver.find_element(By.ID, "exampleInputEmail1").send_keys("selenium_test_user@example.com")
    driver.find_element(By.ID, "exampleInputPassword1").send_keys("Test@1234")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(2)
    assert "Welcome" in driver.page_source or "Blog" in driver.page_source

# 3. Login user
def test_login_user(driver):
    driver.get(f"{BASE_URL}/user/signin")
    driver.find_element(By.ID, "exampleInputEmail1").send_keys("selenium_test_user@example.com")
    driver.find_element(By.ID, "exampleInputPassword1").send_keys("Test@1234")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(2)
    assert "Blog" in driver.page_source or "Welcome" in driver.page_source

# 4. Create blog post
def test_create_blog(driver):
    driver.get(f"{BASE_URL}/user/signin")
    driver.find_element(By.ID, "exampleInputEmail1").send_keys("selenium_test_user@example.com")
    driver.find_element(By.ID, "exampleInputPassword1").send_keys("Test@1234")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(2)

    driver.get(f"{BASE_URL}/blog/add")
    driver.find_element(By.ID, "title").send_keys("Test Blog by Selenium")
    driver.find_element(By.ID, "body").send_keys("This is the body of the test blog created using Selenium.")
    driver.find_element(By.CSS_SELECTOR, "form button.btn-primary").click()
    time.sleep(2)
    assert "Test Blog by Selenium" in driver.page_source

# 5. View blog list and click
def test_view_blog_list(driver):
    driver.get(BASE_URL)
    cards = driver.find_elements(By.CLASS_NAME, "card-title")
    titles = [card.text for card in cards]
    assert any("Test Blog by Selenium" in title for title in titles)

# 6. Add a comment
def test_add_comment(driver):
    driver.get(f"{BASE_URL}/user/signin")
    driver.find_element(By.ID, "exampleInputEmail1").send_keys("selenium_test_user@example.com")
    driver.find_element(By.ID, "exampleInputPassword1").send_keys("Test@1234")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(2)

    driver.get(BASE_URL)
    view_buttons = driver.find_elements(By.LINK_TEXT, "View")
    view_buttons[0].click()
    time.sleep(1)

    comment_input = driver.find_element(By.NAME, "content")
    comment_input.send_keys("This is a test comment from Selenium.")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(1)
    assert "This is a test comment from Selenium." in driver.page_source

# 7. Check blog author's image and name
def test_blog_author_info(driver):
    driver.get(BASE_URL)
    driver.find_elements(By.LINK_TEXT, "View")[0].click()
    time.sleep(1)

    image = driver.find_element(By.CSS_SELECTOR, "img[src*='/images']")
    assert image is not None

# 8. Check comment count display
def test_comment_section(driver):
    driver.get(BASE_URL)
    driver.find_elements(By.LINK_TEXT, "View")[0].click()
    time.sleep(1)

    assert "Comments" in driver.page_source

# 9. Upload image field presence in blog form
def test_blog_upload_field(driver):
    driver.get(f"{BASE_URL}/user/signin")
    driver.find_element(By.ID, "exampleInputEmail1").send_keys("selenium_test_user@example.com")
    driver.find_element(By.ID, "exampleInputPassword1").send_keys("Test@1234")
    driver.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()
    time.sleep(2)

    driver.get(f"{BASE_URL}/blog/add")
    cover_input = driver.find_element(By.ID, "coverImage")
    assert cover_input.get_attribute("type") == "file"

# 10. Blog card view on homepage
def test_homepage_blog_cards(driver):
    driver.get(BASE_URL)
    cards = driver.find_elements(By.CLASS_NAME, "card")
    assert len(cards) > 0
