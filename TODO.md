TODO:
15. Make sure we're all ready to justify our reasonings for the interviews later

DONE:
1. Filter replytocom links
2. Filter www subdomain
3. Treat https and http as same token (https://edstem.org/us/courses/16769/discussion/1051861)
4. Filter calendar elems
5. Print length of the longest page 
6. Make sure not to send entire html just send the url https://edstem.org/us/courses/16769/discussion/1053191
7. Avoid crawling low content websites eg. pages with lots of comments
8. Avoid very large files
9. Use regex to avoid links like https://mt-live.ics.uci.edu/events/list/?tribe-bar-date=2021-04-06&eventDisplay=past with calendars (might already be done with repeated directory logic)
11. Should we adding entire url to url_set or just a part of it? i.e. should we chop off params, scheme, or anything else? Also reevaluate how we're counting our unique pages because we may be adding too many similar links? edit: nvmd I think we're doing this right
13. Make sure not to go too far down the rabithole of https://mt-live.ics.uci.edu/ since it has pages with paths like /2019/11/04 and /events/2021-12-01. Also consider if they're even worth scraping? Most of them are pretty low content
14. Filter out if it's a just not a lot of text/low content in general (might wanna consider finding length of just text for this one) e.g. https://mt-live.ics.uci.edu/events/2021-12-01
10. Avoid repeated pages like one in this post: https://edstem.org/us/courses/16769/discussion/1043467 (might already be done with repeated directory logic)
12. Check Ed post for examples of traps we should deal with: https://edstem.org/us/courses/16769/discussion/1043278 and https://edstem.org/us/courses/16769/discussion/1052843