export const myDemoFunction = defineFunction({
  entry: './demo-function-handler.ts',
  name: 'overrideName' // explicitly set the name to override the default naming behavior
});