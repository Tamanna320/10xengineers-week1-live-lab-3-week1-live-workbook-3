# Tasks

## New Feature Request

Add a **likes feature** to blog posts:

### Requirements:
- Users should be able to like a post
- Each post should track total like count
- Implement `POST /posts/{post_id}/like` endpoint
- Implement `GET /posts/{post_id}/likes` endpoint (returns like count)
- Optional: prevent duplicate likes from same user (by name)

### Implementation Hints:
- Add a `Like` model to models.py
- Add likes storage to storage.py
- Use good prompting strategies learned in class

### Constraints:
- Keep changes minimal and follow existing code patterns
- Don't over-engineer the solution
