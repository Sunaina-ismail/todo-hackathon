# Page snapshot

```yaml
- generic [ref=e1]:
  - generic [ref=e4]:
    - generic [ref=e5]:
      - heading "Welcome back" [level=1] [ref=e6]
      - paragraph [ref=e7]: Enter your email below to sign in to your account
    - generic [ref=e8]:
      - generic [ref=e9]:
        - heading "Sign In" [level=3] [ref=e10]
        - paragraph [ref=e11]: Enter your email and password to access your account
      - generic [ref=e12]:
        - generic [ref=e13]:
          - generic [ref=e14]:
            - text: Email
            - textbox "Email" [active] [ref=e15]:
              - /placeholder: you@example.com
          - generic [ref=e16]:
            - text: Password
            - textbox "Password" [ref=e17]:
              - /placeholder: ••••••••
        - button "Sign in" [ref=e19] [cursor=pointer]
    - paragraph [ref=e20]:
      - text: Don't have an account?
      - link "Sign up" [ref=e21] [cursor=pointer]:
        - /url: /sign-up
  - region "Notifications alt+T"
  - button "Open Next.js Dev Tools" [ref=e27] [cursor=pointer]:
    - img [ref=e28]
  - alert [ref=e31]
```