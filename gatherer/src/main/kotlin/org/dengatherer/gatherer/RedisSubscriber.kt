package org.dengatherer.gatherer

import redis.clients.jedis.Jedis
import redis.clients.jedis.JedisPubSub

class RedisSubscriber {
    fun subscribe() {
        val jedis = Jedis()
        jedis.subscribe(MyListener(), "exposes")
    }
}

class MyListener : JedisPubSub() {
    override fun onMessage(channel: String?, message: String?) {
        println("Received message on channel $channel")
        println(message)
    }
}

fun main() {
    RedisSubscriber().subscribe()
}
