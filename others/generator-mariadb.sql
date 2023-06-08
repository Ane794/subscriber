create table website
(
    id      int auto_increment comment 'ID'
        primary key,
    name    longtext not null comment '名称',
    options json comment '选项',
    comment longtext comment '注释'
) comment '网站';

create table account
(
    id         int auto_increment comment 'ID'
        primary key,
    name       longtext not null comment '名称',
    login_key  longtext not null comment '登录密钥',
    nickname   longtext comment '昵称',
    options    json comment '选项',
    website_id int      not null comment '网站 ID',
    comment    longtext comment '注释',
    constraint account_website_id_fk
        foreign key (website_id) references website (id)
) comment '账号';

create table task
(
    id         int auto_increment comment 'ID'
        primary key,
    name       longtext not null comment '名称',
    options    json comment '选项',
    website_id int      not null comment '网站 ID',
    comment    longtext comment '注释',
    constraint task_website_id_fk
        foreign key (website_id) references account (id)
) comment '任务';

create table execution
(
    id         int auto_increment comment 'ID'
        primary key,
    options    json comment '选项',
    task_id    int not null comment '任务 ID',
    account_id int not null comment '账号 ID',
    comment    longtext comment '注释',
    constraint execution_task_id_fk
        foreign key (task_id) references account (id),
    constraint execution_account_id_fk
        foreign key (account_id) references account (id)
) comment '执行';
