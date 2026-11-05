using System.Reflection.Metadata;
using System.Reflection.PortableExecutable;
using System.Text.Json;

var checks = JsonSerializer.Deserialize<List<Check>>(File.ReadAllText(args[0]))!;
var passed = 0;
foreach (var check in checks)
{
    using var stream = File.OpenRead(Path.Combine(args[1], check.assembly));
    using var pe = new PEReader(stream);
    var reader = pe.GetMetadataReader();
    var type = Find(reader, check.type);
    if (check.method is { } method)
    {
        var definition = type.GetMethods().Select(reader.GetMethodDefinition)
            .Single(x => reader.GetString(x.Name) == method);
        var signature = reader.GetBlobReader(definition.Signature);
        var header = signature.ReadSignatureHeader();
        if (header.IsGeneric) signature.ReadCompressedInteger();
        var count = signature.ReadCompressedInteger();
        var returnType = signature.ReadSignatureTypeCode().ToString();
        if (count != check.parameters || (check.returns is { } expectedReturn && returnType != expectedReturn))
            throw new InvalidDataException($"ABI mismatch: {check.type}.{method}: {count} parameters, return {returnType}");
    }
    else if (check.field is { } field)
    {
        var actual = Offset(reader, type, field);
        using var sdkStream = File.OpenRead(Path.Combine(args[1], "references/upstream-api14-final/FFXIVClientStructs.dll"));
        using var sdkPe = new PEReader(sdkStream);
        var sdk = sdkPe.GetMetadataReader();
        var expected = Offset(sdk, Find(sdk, check.sdkType!), check.sdkField!) + check.delta;
        if (actual != expected)
            throw new InvalidDataException($"Layout mismatch: {check.type}.{field}: 0x{actual:X} vs SDK 0x{expected:X}");
    }
    passed++;
}
Console.WriteLine($"Passed {passed} compiled native ABI/layout contracts against pinned API14 SDK and upstream declarations.");
if (args.Length > 2)
    File.WriteAllText(args[2], JsonSerializer.Serialize(new { status = "passed", count = passed,
        scope = "Compiled metadata comparison; no native execution or TC runtime test", checks },
        new JsonSerializerOptions { WriteIndented = true }) + "\n");

static TypeDefinition Find(MetadataReader reader, string name)
    => reader.GetTypeDefinition(reader.TypeDefinitions.Single(x => Name(reader, x) == name));

static string Name(MetadataReader reader, TypeDefinitionHandle handle)
{
    var type = reader.GetTypeDefinition(handle);
    var parent = type.GetDeclaringType();
    return parent.IsNil ? reader.GetString(type.Namespace) + "." + reader.GetString(type.Name)
        : Name(reader, parent) + "+" + reader.GetString(type.Name);
}

static int Offset(MetadataReader reader, TypeDefinition type, string field)
    => type.GetFields().Select(reader.GetFieldDefinition).Single(x => reader.GetString(x.Name) == field).GetOffset();

record Check(string assembly, string type, string? method = null, int parameters = 0, string? returns = null,
    string? field = null, string? sdkType = null, string? sdkField = null, int delta = 0);
