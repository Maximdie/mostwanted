<?php
/*
 * Вход в админку новостей: https://mostwanted.consulting/admin/
 *
 * Здесь хранится только хеш пароля (сам пароль восстановить из него нельзя).
 * Пароль удобнее менять в самой админке («Сменить пароль») — тогда новый хеш
 * ляжет в _news/data/auth.json на хостинге и будет главнее этого.
 */
return [
    'user' => 'igor',
    'hash' => '$2y$12$XV0n5FL6HdIojvad7/maf.0Y6Mxzl32ZAiT.HpZoPMT3uGY1Wpox2',
];
