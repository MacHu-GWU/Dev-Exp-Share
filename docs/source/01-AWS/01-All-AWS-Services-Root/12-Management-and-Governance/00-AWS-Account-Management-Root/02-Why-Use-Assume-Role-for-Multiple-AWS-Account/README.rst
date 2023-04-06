Why User Assume Role for Multiple AWS Account
==============================================================================

For big Organiztion, **it is always a bad idea to maintain multiple IAM User in different AWS Account representing the same Person**. Because it makes it harder to track activity / cost did by the same person, and also managing multiple sensitive credential may greatly increase the propability of leaking. In addition, assume-role makes it easy to switch between multiple AWS Account, instead of typing credentials.
