from injecta.container.ContainerBuild import ContainerBuild
from injecta.parameter.allPlaceholdersReplacer import findAllPlaceholders, replaceAllPlaceholders
from injecta.service.argument.TaggedAliasedServiceArgument import TaggedAliasedServiceArgument
from injecta.service.argument.ServiceArgument import ServiceArgument
from injecta.service.resolved.ResolvedArgument import ResolvedArgument

class TaggedAliasedArgumentResolver:

    def resolve(self, resolvedArgument: ResolvedArgument, containerBuild: ContainerBuild):
        argument = resolvedArgument.argument

        if not isinstance(argument, TaggedAliasedServiceArgument):
            return resolvedArgument

        servicesForTag = containerBuild.getServicesByTag(argument.tagName)

        if isinstance(argument.tagAlias, str):
            value = self.__resolveParameterValue(argument.tagAlias, containerBuild.parameters)
        else:
            value = argument.tagAlias

        for service in servicesForTag:
            tagAttributes = service.getTagAttributes(argument.tagName)

            if 'alias' not in tagAttributes:
                raise Exception(f'"alias" attribute is missing for tag {argument.tagName}')

            if tagAttributes['alias'] == value:
                resolvedArgument.modifyArgument(ServiceArgument(service.name, argument.name), 'service by tag alias')
                return resolvedArgument

        raise Exception(f'No service found for type: {value}')

    def __resolveParameterValue(self, argument, parameters):
        matches = findAllPlaceholders(argument)

        if not matches:
            return argument

        return replaceAllPlaceholders(argument, matches, parameters, argument)
