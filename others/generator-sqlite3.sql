create table website
(
    id      integer not null
        constraint website_pk
            primary key autoincrement,
    name    text    not null,
    options text,
    comment text
);

create table account
(
    id         integer not null
        constraint account_pk
            primary key autoincrement,
    name       text    not null,
    login_key  text    not null,
    nickname   text,
    options    text,
    website_id integer not null
        constraint account_website_id_fk
            references website,
    comment    text
);

create table task
(
    id         integer not null
        constraint task_pk
            primary key autoincrement,
    name       text    not null,
    options    text,
    website_id integer not null
        constraint task_website_id_fk
            references website,
    comment    text
);

create table execution
(
    id         integer not null
        constraint execution_pk
            primary key autoincrement,
    options    text,
    task_id    integer not null
        constraint execution_task_id_fk
            references task,
    account_id integer not null
        constraint execution_account_id_fk
            references account,
    comment    text
);
