create table website
(
    id      integer not null
        constraint website_pk
            primary key autoincrement,
    name    text    not null,
    options text
);

create table account
(
    id         integer not null
        constraint account_pk
            primary key autoincrement,
    name       text    not null,
    login_key  text    not null,
    nickname   text default name,
    options    text,
    website_id integer not null
        constraint account_website_id_fk
            references website
);

create table work
(
    id         integer not null
        constraint work_pk
            primary key autoincrement,
    name       text    not null,
    options    text,
    account_id integer not null
        constraint work_account_id_fk
            references account
);
