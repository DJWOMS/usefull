# Chat 
#### url

     ws://${window.location.host}/ws/chat/room/?token=${localStorage.getItem('Token')}

##Actions

- example


    pk: 15,
    action: "join_room",
    request_id: new Date().getTime()


#### Присоединиться к комнате - join_room

    pk: room_id,
    action: "join_room",
    request_id: request_id

#### После присоединения к комнате - retrieve
- Request


    pk: room_pk,
    action: "retrieve",
    request_id: request_id

- Response


    {
      "errors": [],
      "data": {
        "pk": 4,
        "name": "Python",
        "user": 29,
        "team": null,
        "messages": [
          {
            "id": 1,
            "created_at_formatted": "02-12-2021 10:29:38",
            "user": {
              "id": 47,
              "username": "djwoms1",
              "avatar": "/media/default/default.jpg",
              "github": ""
            },
            "text": "мое сообщение",
            "create_date": "2021-12-02T13:29:38.171083+03:00",
            "room": 4
          },
        ],
        "member": [
          {
            "id": 47,
            "username": "djwoms1",
            "avatar": "/media/default/default.jpg",
            "github": ""
          }
        ]
      },
      "action": "retrieve",
      "response_status": 200,
      "request_id": 1638979242972
    }

#### Подписаться на получения сообщений в чате - subscribe_to_messages_in_room

    pk: room_pk,
    action: "subscribe_to_messages_in_room",
    request_id: request_id

#### Подписаться на изменения в комнате - subscribe_instance

    pk: room_pk,
    action: "subscribe_instance",
    request_id: request_id

#### Отправить сообщение - create_message
- Request


    message: message,
    action: "create_message",
    request_id: request_id


#### Получить сообщение - create
- Response


    {
      "data": {
        "id": 28,
        "user": {
          "id": 29,
          "username": "string",
          "avatar": "/media/default/default.jpg",
          "github": ""
        },
        "text": "Hi world!!!",
        "create_date": "2021-12-08T19:34:41.242824+03:00",
        "room": 4
      },
      "action": "create",
      "pk": 28
    }

#### Покинуть комнату - leave_room

    pk: room_pk,
    action: "leave_room",
    request_id: request_id


### Любое действие в комнате которое не описано выше - default

#### Другой пользователь присоединился к комнате

    {
      "join_user": [
        {
          "id": 47,
          "username": "djwoms1",
          "avatar": "/media/default/default.jpg",
          "github": ""
        }
      ]
    }














