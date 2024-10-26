-- Docs: https://docs.mage.ai/guides/sql-blocks
SELECT object__url 
FROM money_diaries.diary_links__rows__entities 
where type = 'blog_entry';
