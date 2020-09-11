<template>
  <div class="vue-app">
                                <!-- Event -->
        <!-- <h1>Events</h1> 
        <button @click.once="add(1)">Add</button>
        <button @click="subtract(1)">Subtract</button>
        <button @dblclick="add(10)">Add 10</button>
        <button @dblclick="subtract(10)">Subtract 10</button>
        <p>Number is: {{num}} </p>
        <a @click.prevent="click" href="http://www.google.com">Hello</a> -->
        <!-- <p> {{test()}} </p> -->


                                <!-- <h1>Keyboard Events</h1>
        <label>Name: </label>
        <input type="text" v-model="name"><br><br>
        <span>{{name}}</span>
        <label>Age: </label>
        <input type="text" v-model="age" placeholder="hello from the otherside">
        <span>{{age}}</span> -->


                                <!-- <h1>Computed Properties</h1> -->
        <button @click="a++">Add to A</button>
        <button @click="b++">Add to B</button>
        <p>A - {{a}}</p>
        <p>B - {{b}}</p>
        <p>Age + A = {{addtoA}} </p>
        <p>Age + B = {{addtoB}} </p>
  </div>
</template>

<script>
export default {
    data() {
        return {
            // name: '',
            age: 20,
            a: 0,
            b: 6

        }
    },

    methods: {
        // add(inc) {
        //     this.num += inc
        // },

        // subtract(dec){
        //     this.num -= dec
        // },

        // click() {
        //     alert('SUPRISE MOTHER FUCKER')
        // }

        // logName() {
        //     console.log('Name entered') 
        // },

        // logAge() {
        //     console.log('Age entered')
        // }

    },


    computed: {
        addtoA() {
            console.log('A added')
            return this.a + this.age
        },

        addtoB() {
            console.log('B added')
            return this.b + this.age
        }
    }
}
</script>

<style>

</style>