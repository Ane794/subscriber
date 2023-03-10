create table website
(
    id      int auto_increment comment '网站 ID'
        primary key,
    name    longtext not null comment '网站名称',
    options json comment '网站选项',
) comment '网站';

create table account
(
    id         int auto_increment comment '账号 ID'
        primary key,
    name       longtext not null comment '账号名称',
    login_key  longtext not null comment '登录密钥',
    nickname   longtext comment '账号昵称',
    options    json comment '账号选项',
    website_id int      not null comment '网站 ID',
    constraint account_website_id_fk
        foreign key (website_id) references website (id)
) comment '账号';

create table work
(
    id         int auto_increment comment '任务 ID'
        primary key,
    name       longtext not null comment '任务名称',
    options    json comment '任务选项',
    account_id int      not null comment '账号 ID',
    constraint work_account_id_fk
        foreign key (account_id) references account (id)
) comment '任务';
