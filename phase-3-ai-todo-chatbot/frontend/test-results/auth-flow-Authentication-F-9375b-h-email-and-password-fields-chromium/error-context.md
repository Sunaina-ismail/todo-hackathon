# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - generic [ref=e4]:
    - generic [ref=e5]:
      - heading "Create an account" [level=1] [ref=e6]
      - paragraph [ref=e7]: Enter your details below to create your account
    - generic [ref=e8]:
      - generic [ref=e9]:
        - heading "Create Account" [level=3] [ref=e10]
        - paragraph [ref=e11]: Enter your details to create a new account
      - generic [ref=e12]:
        - generic [ref=e13]:
          - generic [ref=e14]:
            - text: Email
            - textbox "Email" [ref=e15]:
              - /placeholder: you@example.com
          - generic [ref=e16]:
            - text: Password
            - textbox "Password" [ref=e17]:
              - /placeholder: ••••••••
            - paragraph [ref=e18]: Must be at least 8 characters
          - generic [ref=e19]:
            - text: Confirm Password
            - textbox "Confirm Password" [ref=e20]:
              - /placeholder: ••••••••
        - button "Create account" [ref=e22] [cursor=pointer]
    - paragraph [ref=e23]:
      - text: Already have an account?
      - link "Sign in" [ref=e24] [cursor=pointer]:
        - /url: /sign-in
  - region "Notifications alt+T"
  - button "Open Next.js Dev Tools" [ref=e30] [cursor=pointer]:
    - img [ref=e31]
  - alert [ref=e34]
```