# dadataScrypt
Scrypt can accept limitless count of arguments, but first one can be only uid. Others - adresses which need to be normalized. Requires the use of quotes in every request.
After executing the script, the results are written to a hml file named uid.

Example of log file:
Every query starts with "==..." adn ends by "==..." + uid or "with error" (depends on the result)

2021-11-16T10:55:54.946022+0300 INFO ============================================
2021-11-16T10:55:54.946998+0300 CRITICAL There is no uid in arguments
2021-11-16T10:55:54.946998+0300 INFO ============================================ with error
2021-11-16T10:56:30.540451+0300 INFO =======================================================
2021-11-16T10:56:30.543378+0300 WARNING No addresses in arguments which should contains address. XML doesn't generated
2021-11-16T10:56:30.543378+0300 INFO ============================================ with error
2021-11-16T10:56:58.832437+0300 INFO =======================================================
2021-11-16T10:56:58.926132+0300 WARNING Dadata returns null result because of bad query. Query: Сан-Франциско, улица Ленина 4
2021-11-16T10:56:58.932964+0300 INFO Created xml document with id test
2021-11-16T10:56:58.933941+0300 INFO ============================================ test
2021-11-16T10:57:35.728298+0300 INFO =======================================================
2021-11-16T10:57:35.879577+0300 INFO Created xml document with id test1
2021-11-16T10:57:35.880554+0300 INFO ============================================ test1
2021-11-16T10:57:50.337434+0300 INFO =======================================================
2021-11-16T10:57:50.429177+0300 WARNING Dadata returns null result because of bad query. Query: Улица Шувалова дом 2 квартира 356 Мурино
2021-11-16T10:57:50.435317+0300 INFO Created xml document with id test2
2021-11-16T10:57:50.436010+0300 INFO ============================================ test2
2021-11-16T10:58:21.396437+0300 INFO =======================================================
2021-11-16T10:58:21.527891+0300 INFO Created xml document with id test2
2021-11-16T10:58:21.528868+0300 INFO ============================================ test2
2021-11-16T10:59:28.401682+0300 INFO =======================================================
2021-11-16T10:59:28.481243+0300 CRITICAL Query error (dadata), query uid is test2 Client error '403 Forbidden' for url 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address'
For more information check: https://httpstatuses.com/403
2021-11-16T10:59:28.483195+0300 INFO ============================================ with error
