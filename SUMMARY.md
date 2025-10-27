# Summary of Work Done

During the test task, an automated UI testing framework was implemented using the **Page Object** pattern and best practices for maintainability and reliability. The following key decisions and approaches were made:

- A **BasePage** class was created as a foundation for all page objects. It centralizes common functionality (navigation, element interactions, waiting) and reduces code duplication.  

- For element interactions, the framework consistently uses  
  `WebDriverWait(...).until(EC...)` expected conditions instead of calling element functions directly (`click()`, `send_keys()`, `is_displayed()`).  
  This ensures that actions like typing text, clicking buttons, or checking visibility are performed only when the element is present and interactable.  
  Using timed, retrying checks makes the tests much more stable on dynamic pages compared to immediate direct calls, which can easily fail if the DOM has not yet updated.  

- A simple `config.py` file was used for configuration. This allows quick access to parameters (URLs, credentials, timeouts) without additional dependencies. Alternatives such as `.env` files or `config.ini` could be used in the future for greater flexibility, especially with multiple environments.  

- **Composition** was applied for injecting reusable components such as the **login form** (used in guest and `/accounts` pages).  
  - This approach reduces code duplication and keeps shared UI elements in one place, so changes to the component are reflected everywhere it is used.  
  - In this case, **inheritance** could also be used (e.g., creating a `BaseLoginPage`), but composition was chosen for greater flexibility and to avoid a rigid class hierarchy.

- A **dynamic locator builder inside components** was introduced to handle repeated structures like post articles in the feed.  
  - Instead of caching `WebElement` references (which quickly become stale in Instagram’s constantly refreshing DOM), the framework generates fresh XPath locators for each interaction.  
  - Example: `"//article[1]//*[@aria-label='Like']"` is constructed when interacting with the first post.  
  - This approach (sometimes called **dynamic locator composition**) ensures tests always interact with the current DOM, reducing flaky failures from re-rendered or updated elements.  

- **Retries for unstable elements:**  
  Functions like `safe_click` and `type_text` implement retry logic with `StaleElementReferenceException` handling.  
  - If an element goes stale mid-action (common on dynamic feeds), the framework automatically retries the interaction a few times before failing.  
  - This makes tests more robust and minimizes flaky failures caused by DOM refreshes.

- For the **tests/test_signup.py**, negative scenario was chosen (invalid email). This decision was made because the application under test is a real production system (Instagram), and creating actual accounts in production is not practical. In a proper test environment, positive scenarios (successful account creation) would normally be prioritized, with possible clean up functions.
  - Additionally, **parameterization** can be applied here to validate multiple invalid input combinations (e.g., missing fields, invalid email formats, weak passwords) efficiently, extending coverage without duplicating code.  

- For the **tests/login.py**, a **parameterized approach** was used.  
  - This improves maintainability by avoiding duplicate test code.  
  - It increases coverage by allowing multiple input combinations (valid and invalid credentials, edge cases, etc.) to be tested efficiently in a single test structure.  
  - The datasets currently used for parameterization are **example ones**, but they can be easily extended with more variations (e.g., different username/password combinations, special characters, empty fields) to validate a wider range of login scenarios.  

- **Custom pytest markers** were added to enable flexible test grouping.

- **Structured logging for observability and debugging:**  
  Added informative logs around key actions (navigation, waits, clicks, typing, scroll/hover) in `BasePage` and component methods.  
  - Logs include element/locator details and retry attempts, which speeds up triage of flaky failures.  
  - Provides a clear execution trace in CI and local runs without stepping through the debugger.  

- The overall architecture was designed for modularity, scalability, and readability, so that new pages and test cases can be easily added and maintained.  

---

## Reasons for Decisions

- **Test reliability:** 
  - Using `WebDriverWait(...).until(...)` ensures stability on dynamic pages and avoids flaky tests.
  - Dynamic locator composition: By generating locators dynamically inside component objects, the framework avoids stale element references in constantly changing feeds like Instagram.  
  - Retry strategy for flaky DOM states: `safe_click` and `type_text` automatically retry when a `StaleElementReferenceException` occurs, reducing flaky test failures.  
- **Reduced duplication & better maintainability:** Shared logic is abstracted into `BasePage` and reusable components (like the login form, post article).  
- **Simple configuration:** `config.py` keeps things lightweight for a test task. In a larger project, external config files (`.env`, `config.ini`) would be more appropriate.  
- **Scalable architecture:** Combining composition with the option of inheritance makes the framework flexible for future growth.  
- **Readability:** Code is structured so new contributors can quickly understand page objects, shared utilities, and how to extend tests.
- **Observability:** Structured logging makes test execution transparent, reduces time-to-diagnose for failures.  

